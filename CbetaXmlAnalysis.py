##---------------------------------------------------------------------------------------###
#Cbeta Xml-p5
#Data Source:https://github.com/cbeta-org/xml-p5
#
###--------------------------------------------------------------------------------------###
import datetime
import os
import re
import sys
import time
#-------------------------------------------------------------------------------------------
DEBUG=False
# DEBUG=True
Write = True
Path='xml-p5-master\\T'
puncPattern=r'(\w|[　─❥│\-【 】《》〔〕（）「」『』]|<.{0,5}>)'
#-------------------------------------------------------------------------------------------
# Mylog = ' '
def main(base=1761,lens=1):   
    # subf=['B','GA','N','T','ZW']
    fileList = []
    for dirpath, dirnames, filenames in os.walk(Path):
        for file in filenames:
            if file.endswith('.xml'):
                fileList.append(os.path.join(dirpath, file))

    top=base+lens
    if lens==-1:
        top=len(fileList)

    for i in range(base,top,1):
        data=readFile(fileList[i])
        process(data,fileList[i])
        tim=str(datetime.datetime.now())[0:-7]
        print(tim,' ---> ',str(i+1).rjust(3,'0'),'/',len(fileList),'---$:',fileList[i])
            
        # writeFile('log.txt',Mylog)

#==========================================================  
def preProcess(data):
    data=getStr(data,'<body>','</body>')
    data=data.replace('\n','')
    data=re.sub(r'	','',data) 

    data=re.sub(r'<!--.+?-->','',data)
    data=re.sub(r'<cb:docNumber>(.|\n)+?</cb:docNumber>','',data)
    data=re.sub(r'<anchor xml.+?/>','',data)
    data=re.sub(r'<byline.+?>','<p>',data)
    data=re.sub(r'</byline>','',data)
    data=re.sub(r'<head>','<p>',data)
    data=re.sub(r'</head>','',data)
    data=re.sub(r'<cb:div type="jing">','<p>',data)
    data=re.sub(r'<cb:div type="w">(.|\n)+?</cb:div>','',data) 
    data=re.sub(r'<cb:div type="pin">','<p>',data)
    data=re.sub(r'<cb:jhead type="pin">','<p>',data)    
    data=re.sub(r'<cb:div type="other">.+?>題解<(.|\n)+?</cb:div>','',data) 
    data=re.sub(r'<cb:div type="dharani">(.|\n)+?</cb:div>','\n\n',data)#</cb:div>
    data=re.sub(r'<cb:div.+?type=.+?>','\n\n',data)#</cb:div> 
    data=re.sub(r'</?title>','',data)
    data=re.sub(r'</?cb:jhead>','',data)    
    data=re.sub(r'<cb:juan.+?fun="open.+?>','<juan>',data)    
    data=re.sub(r'<cb:juan.+?</cb:juan>','',data)
    data=re.sub(r'</cb:juan>','',data)
    data=re.sub(r'<cb:mulu.+?</cb:mulu>','',data)  
    data=re.sub(r'(<cb:dialog type(.|\n)+?>|</cb:dialog>)','',data)
    data=re.sub(r'<anchor type="circle"/>','',data)
    data=re.sub(r'<table(.|\n)+?</table>','',data)
    data=re.sub(r'<date>(.|\n)+?</date>','',data)
    data=re.sub(r'<formula(.|\n)+?</formula>','',data)
    data=re.sub(r'(<sp cb:type(.|\n)+?>|</sp>)','',data)
    data=re.sub(r'</?cb:event>','',data)
    data=re.sub(r'<unclear></unclear>','',data)
    data=re.sub(r'(<list>|</list>)','',data)
    data=re.sub(r'(<item xml.+?>|</item>)','',data)
    data=re.sub(r'<lb.+?ed=.+?/>','',data)
    data=fullyDel('<entry','</entry>',data)   
    #--------------------------------------------------------------------------
    data=re.sub(r'<p cb:type="head.+?>','',data) 
    data=re.sub(r'<p cb:type="pre.+?</p>','',data) 
    data=re.sub(r'<p xml.+?>','<p>',data)
    data=re.sub(r'<lb.+?ed=.+?/>','',data)
    data=re.sub(r'<pb (xml:id=.+?)?(n=.+?)?ed=.+?/>','',data)
    data=re.sub(r'(<lg (xml:id=|rend|type=).+?>|</lg>)','',data)
    data=re.sub(r'<note place="inline">','（',data)
    data=re.sub(r'</note>','）',data)
    data=re.sub(r'<ref target="#PTS(.|\n)+?</ref>','',data)
    data=re.sub(r'<label type=(.|\n)+?</label>','',data)
    data=re.sub(r'<head.+?</head>','',data)  
    data=re.sub(r'<milestone.+?(unit="juan")?/>','',data)
    data=re.sub(r'</?cb:div>','',data)       
    data=re.sub(r'<space quantity.+?/>','',data)
    data=re.sub(r'<l rend=".+?>','',data) 
    data=re.sub(r'</?l>','',data)
    data=re.sub(r'<figure>.+?</figure>','',data) 
    #--------------------------------------------------------------------------
    data=re.sub(r'<trailer>(.|\n)+?</trailer>','',data) 
    data=re.sub(r'[\u25a1]','',data) 
    data=re.sub(r'[△○﹂※★]','',data)
    data=re.sub(r'(</?cb:tt?>|<cb:tt? .+?>|</?cb:yin>|</?cb:fan>|</?cb:zi>|</?cb:sg>)','',data)
    data=re.sub(r'<cb:t xml:lang="sa-Sidd">.+?/cb:t>','',data) 
    data=re.sub(r'(<note.+?>|</note>)','',data) 
    data=re.sub(r'(<term xml:lang="sa\-Sidd">|</term>)','',data)

    return data


def process(data,path):
    path='Result'+path[path.find('\\'):]
    path=re.sub(r'[A-Z]{1,2}\d{2,3}\\','',path)

    # if DEBUG and Write:
    #     tdata=re.sub(r'(\W|[0-z])','',data)
    #     addr=path.replace('.xml','-T.xml')
    #     writeFile(addr,tdata)

    # if DEBUG and Write:
    #     bdata=getStr(data,'<body>','</body>')
    #     addr=path.replace('.xml','-B.xml')
    #     writeFile(addr,bdata)

    mlist=createMap(data)
    data=preProcess(data)
    data=replaceCB(data,mlist)
    data=dharani(data)
    data=lastProcess(data)

    if DEBUG and Write:
        addr=path.replace('.xml','-D.h.xml')
        writeFile(addr,data)

    if DEBUG and Write:
        pdata=re.sub(puncPattern,'',data)
        addr=path.replace('.xml','-P.txt')
        writeFile(addr,pdata)  

    data=checkPunc(data)
    if Write:
        if len(data)>50:
            addr=path.replace('.xml','_out.xml')
            writeFile(addr,data)
    
    if DEBUG:
        ldata=re.sub(r'(<p>|<juan>)','',data)
        pattern=re.compile(r'<.+?>')
        lis=pattern.findall(ldata)
        if len(lis)>0:
            print(lis[0])
    
    # output(data,path)

def output(dat,path):
    dat=re.sub(r'(<p>|\n)','',dat)
    dat=re.sub(r'<juan>','\n',dat)
    dat=dat.lstrip('\n').rstrip('\n')
    addr=path.replace('.xml','.out').replace('Result','TrainData')
    writeFile(addr,dat)     

def lastProcess(data):
    data=re.sub(r'(</p>)','',data)
    data=re.sub(r'<p>','###',data)
    data=re.sub(r'<juan>','$$$',data)    
    data=re.sub(r'(<.+?>)','',data)    
    data=re.sub(r'###','<p>',data)
    data=re.sub(r'\$\$\$','\n<juan>',data)
    data=data.lstrip('\n').rstrip('\n')
    # data=re.sub(r'：<p>','：',data)
    data=re.sub(r'\n+','\n',data)
    data=re.sub(r'　+','　',data)
    data=re.sub(r'　','<#sp>',data)

    data=re.sub(r'(<p>)+','<p>',data)
    data=re.sub(r'\n?<p>\n?','<p>',data)   
    data=re.sub(r'<.+?><','<',data)
    
    return data

def checkPunc(data):
    sdata=data.split('<juan>')
    for i in range(len(sdata)):
        s=sdata[i]
        if s=='':
            continue

        es=re.sub(puncPattern,'',s)#有效符号
        if len(es)!=0:            
            puncPercent=len(es)/len(s)
            periodPercent=es.count('。')/len(es)
            nJudou=1-len(es.replace('。','').replace('．',''))/len(es)            
            # print(50*'-','>')
            # print('punc/len: ',len(es),'/',len(s)  ,'  ',puncPercent)
            # print('period/len: ',es.count('。'),'/',len(es)  ,'  ',periodPercent)
            # print('njudou/len: ',len(es.replace('。','').replace('．','')),'/',len(es)  ,'  ',nJudou)

            if puncPercent<0.08:
                s=''
            if periodPercent>0.9:
                s=''
            if nJudou>0.9:
                s=''
        else:
            s=''

        if s!='' and s.endswith('，')==False and s.endswith('。')==False and s.endswith('！')==False and s.endswith('？')==False and s.endswith('」')==False and s.endswith('』')==False:
            s+='。'

        sdata[i]=s
    data='\n<juan>'.join(sdata)    
    data=re.sub(r'(<juan>\n)+','<juan>',data)
    # data=re.sub(r'\n+','\n',data)
    data=data.lstrip('\n').rstrip('\n')
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
        c=mlis[i][1]
        if c!='':
            if len(c)>=5:
                c='❥'
            else:
                c= chr(eval( '0x'+mlis[i][1].rjust(8,'0')))
        else:
            c=mlis[i][2]
            if len(c)>=5:
                c='❥'
        data=re.sub(r'>.{1,2}</g>','><$',data)
        data=data.replace('<g ref="#'+mlis[i][0]+'"><$',c) 
    return data

def dharani(data):
    while data.find('<p cb:type="dharani" xml:id=')!=-1:
        d=getStr(data,'<p cb:type="dharani" xml:id=','</p>','w')       
        r=re.sub(r'<p cb:type="dharani" xml:id=.+?>','<p>',d)
        data=data.replace(d,r)
    return data

#==========================================================
def fullyDel(head,tial,data):
    while data.find(head)!=-1:
        h=data.rfind(head)
        hdata=data[0:h]
        tdata=data[h:]
        t=tdata.find(tial)+len(tial)
        tdata=tdata[t:]
        data=hdata+tdata
    return data

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
    x=1
    y=1
    if len(sys.argv) > 2:       
        y=sys.argv[2]
        y = int(y)
        x = sys.argv[1]
        x = int(x)-1    
        main(x,y) 
    elif len(sys.argv) > 1: 
        x = sys.argv[1]
        x = int(x)-1 
        main(x,y)       
    else:
        main() 
#==========================================================


