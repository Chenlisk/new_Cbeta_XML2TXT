###------------------------------------------------------------------------------------------------###
#Cbeta Xml-p5
#Data Source:https://github.com/cbeta-org/xml-p5
#
###------------------------------------------------------------------------------------------------###
import datetime
import os
import re
import sys
import time

def main(base=0):
    path='xml-p5-master\\T'
    fileList = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if file.endswith('.xml'):
                 fileList.append(os.path.join(dirpath, file))

    top=len(fileList)
    top=base+15

    for i in range(base,top):
        data=readFile(fileList[i])
        process(data,fileList[i])
        print(str(i+1).rjust(3,'0'),'/',len(fileList),'---$:',fileList[i])

#==========================================================    
def preProcess(data):
    data=getStr(data,'<body>','</body>')
    data=data.replace('\n','')
    data=re.sub(r'	','',data)

    data=re.sub(r'<cb:docNumber>.+?</cb:docNumber>','',data)
    data=re.sub(r'<anchor xml.+?/>','',data)
    data=re.sub(r'<byline cb.+?</byline>','',data)
    data=re.sub(r'<head>.+?</head>','',data)
    data=re.sub(r'<cb:juan.+?</cb:juan>','',data)
    data=re.sub(r'<cb:mulu.+?</cb:mulu>','',data)
    data=re.sub(r'<anchor type="circle"/>','',data)
    #--------------------------------------------------------------------------
    data=re.sub(r'<cb:div type=.+?>','\n\n',data)#</cb:div>
    data=re.sub(r'<p xml.+?>','<p>',data)
    data=re.sub(r'<lb.+?ed=.+?/>','',data)
    data=re.sub(r'<pb (xml:id=.+?)?(n=.+?)?ed=.+?/>','',data)
    data=re.sub(r'(<lg (xml:id=|rend).+?>|</lg>)','',data)
    data=re.sub(r'<note place="inline">.+?</note>','',data)
    data=re.sub(r'<cb:tt>.+?</cb:tt>','',data)  
    data=re.sub(r'<head.+?</head>','',data)  
    data=re.sub(r'<milestone.+?(unit="juan")?/>','',data)
    data=re.sub(r'</cb:div>','',data)       
    data=re.sub(r'<space quantity.+?/>','',data)
    data=re.sub(r'<l rend="text-indent.+?>','<l>',data) 

    # data=re.sub(r'</l><p>','</p>\n<p>',data)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    # data=re.sub(r'</p><l>','',data)      
    data=re.sub(r'(</l><l>)','',data)
    # data=re.sub(r'(</l>|<l>)','',data)

    # data=re.sub(r'</p><p>','</p>\n<p>',data) 
    # data=re.sub(r'</p><p cb:type','</p>\n<p cb:type',data) 
    # data=re.sub(r'：</p>\n?<p>','：',data) 
    
    #    data=re.sub(r'','',data) 
    #    data=re.sub(r'','',data) 
    #    data=re.sub(r'','',data) 
    #    data=re.sub(r'','',data) 
    #    data=re.sub(r'','',data) 
    #    data=data.replace('</l><p>','</p>\n<p>')
    #    data=data.replace('</p><l>','')
    return data

def process(data,path):
    tdata=re.sub(r'(\W|[0-z])','',data)
    addr='Result'+path[path.rfind('\\'):].replace('.xml','.txt')
    writeFile(addr,tdata)

    mlist=createMap(data)
    data=preProcess(data)
    data=replaceCB(data,mlist)
    data=dharani(data)
    data=lastProcess(data)

    addr='Result'+path[path.rfind('\\'):]
    writeFile(addr,data)

def lastProcess(data):
    data=re.sub(r'\n<p></p>\n+','',data) 

    data=re.sub(r'　','',data)


    # data=re.sub(r'<p>.+?</p>\n?','',data)#---------------------------------------test
    data=re.sub(r'\n\n+','\n\n',data)   

    return data

def createMap(data):
    mlist=[]
    data=getStr(data,'<charDecl>','</charDecl>','w')
    mlis=data.split('</char>')

    for i in range(len(mlis)):
        m=mlis[i].replace('\n','')
        cb=getStr(m,'xml:id="','"')#CB
        if cb =='':
            continue
        ucode=getStr(m,'unicode">U+','</mapping>')
        nform=getStr(m,'normalized form</localName>','</value>')
        nform=re.sub(r'.+?<value>','',nform)
        if ucode=='' and nform=='':
            nform='❥'
        mlist.append((cb,ucode,nform))
    # print(mlist)
    return mlist

def replaceCB(data,mlis):
    #   <g ref="#CB00006">𤦲</g>       
    for i in range(len(mlis)):
        if mlis[i][1]!='':
            c= chr(eval( '0x'+mlis[i][1].rjust(8,'0')))
        else:
            c=mlis[i][2]
        data=re.sub(r'>.{1,2}</g>','><$',data)
        data=data.replace('<g ref="#'+mlis[i][0]+'"><$',c) 
    return data

def dharani(data):
    while data.find('<p cb:type="dharani" xml:id=')!=-1:
        d=getStr(data,'<p cb:type="dharani" xml:id=','</p>','w')
        r=d.replace('　','，')
        r=r.replace('』</p>','。』</p>')
        r=re.sub(r'<p cb:type="dharani" xml:id=.+?>','<p>',r)
        data=data.replace(d,r)
    return data

#==========================================================
def getStr(data,head,tial,width='n'):
    if data.find(head)==-1 or data.find(head) ==-1:
        return ''

    if width=='w':
        h=data.find(head)
        da=data[h:]
        t =h+da.find(tial)+len(tial)
    else:
        h=data.find(head)+len(head)
        da=data[h:]
        t =h+da.find(tial)
    return data[h:t]


def  readFile(filedir):
    with open(filedir, "r", encoding='utf-8') as f :
        string = f.read()
    return string

def writeFile(filedir, string):
    if filedir.find('\\') != -1:
        path = filedir[0:filedir.rfind("\\")]
        if not os.path.exists(path):
            os.makedirs(path) 
    with open(filedir, "w+", encoding='utf-8') as f:
        f.write(string)
#==========================================================
if __name__ == '__main__':
    if len(sys.argv) > 1:
        x = sys.argv[1]
        x = int(x)
        main(x-1)
    else:
        main()    
#==========================================================