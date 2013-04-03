# -*- coding: utf-8 -*-

#####
# grab google scholar data of GSLIS faculty
# designed by Qiyuan Liu on 1/31/2013
# http://liuqiyuan.com
#####

import urllib2
import re
import os
import HTMLParser


    
class metadataExtraction:      
    # get source
    def getSource(self,urlList):
        """ grap the web page source """
        content=""
        for url in urlList:
            req=urllib2.urlopen(url)
            newcontent=req.read()
            content+=newcontent
        return content

    # extract the title and link
    def getLink(self,content):
        linkDict={}
        pattern='<td id="col-title">(.*?)</td>'
        matchList=re.findall(pattern,content)
        for l in matchList:
            pattern_link='<a href="(.*?)" class="cit-dark-large-link"'
            pattern_title='<a href=".*" class="cit-dark-large-link">(.*?)</a>'
            ml_link=re.findall(pattern_link,l)
            ml_title=re.findall(pattern_title,l)
            if(len(ml_link)>0 and len(ml_link)>0):
                linkDict[ml_title[0]]=ml_link[0]
            else:continue
        return linkDict

    def getMetadata(self,content):
        metaList=[]
        pattern_author='<div class="cit-dt">Authors</div><div class="cit-dd">(.*?)</div>'
        pattern_title='<div id="title"><a style="text-decoration:none" href="(.*?)" >(.*?)</a>'
        pattern_date='<div class="g-section" id="pubdate_sec"><div class="cit-dt">Publication date</div><div class="cit-dd">(.*?)</div></div>'
        pattern_source='<div class="g-section" id="venue_sec"><div class="cit-dt">Journal name</div><div class="cit-dd">(.*?)</div>'
        pattern_discription='<div class="cit-dt">Description</div><div class="cit-dd">(.*?)</div>'
        
        ml_author=re.findall(pattern_author,content)
        ml_title=re.findall(pattern_title,content) # title & original link
        #print ml_title
        ml_date=re.findall(pattern_date,content)
        ml_source=re.findall(pattern_source,content)
        ml_discription=re.findall(pattern_discription,content)
        
        metaList.append(ml_author)
        metaList.append(ml_title)
        metaList.append(ml_date)
        metaList.append(ml_source)
        metaList.append(ml_discription)
        return metaList

    def writeFile(self,fileName,metaListCollection):
        f=open(os.getcwd()+"/"+fileName,'wb')
        ls=[]
        author=""
        originalLink=""
        title=""
        date=""
        source=""
        description=""
        for metaList in metaListCollection:
            #print metaList
            author=metaList[0][0]
            if(len(metaList[1])>0):
                originalLink=metaList[1][0][0]
            if(len(metaList[1])>0):
                title=metaList[1][0][1]
            if(len(metaList[2])>0):
                date=metaList[2][0]
            if(len(metaList[3])>0):
                source=metaList[3][0]
            if(len(metaList[4])>0):
                description=metaList[4][0]
            tupleLine=author+"\t"+title+"\t"+date+"\t"+source+"\t"+originalLink+"\n"
            print tupleLine
            #tupleLine=HTMLParser.HTMLParser().unescape(tupleLine)
            ls.append(tupleLine)
        content="".join(ls)
        #print content
        f.write(content)
        f.close()
        print "The .tsv file has been written successfully!"

    def mainProcess(self,url,fileName):
        dict_link=self.getLink(self.getSource(url))
        metaListCollection=[]
        for title,link in dict_link.iteritems():
            subLink=[("http://scholar.google.com"+link).replace('&amp;','&')]
            #print subLink
            subcont=me.getSource(subLink)
            metaList=me.getMetadata(subcont)
            metaListCollection.append(metaList)
        self.writeFile(fileName,metaListCollection)
             

if __name__ == "__main__":
    #test url list
    url_vetle=["http://scholar.google.com/citations?hl=en&user=omG2Pg8AAAAJ&view_op=list_works&pagesize=100"]
    url_MichaelTwidale=["http://scholar.google.com/citations?hl=en&user=7d8SBR4AAAAJ&view_op=list_works&pagesize=100",
                        "http://scholar.google.com/citations?hl=en&user=7d8SBR4AAAAJ&pagesize=100&view_op=list_works&cstart=100",
                        "http://scholar.google.com/citations?hl=en&user=7d8SBR4AAAAJ&pagesize=100&view_op=list_works&cstart=200"]

    me=metadataExtraction()
    me.mainProcess(url_vetle,"VetleTorvik.csv")
    
    

    


    
    
    


