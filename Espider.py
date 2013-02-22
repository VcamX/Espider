# -*- coding: utf-8 -*-
import StringIO
import lxml.html
from lxml import etree
import urllib2
from selenium import webdriver

# -1: 获取内容失败
class Espider():
    def __init__(self, url, code = "utf-8", option = 2):
        self.content = self.fetchContent(url, code, option)
        self.tree = self.buildTree(self.content)
    
    def fetchContent(self, url, code = "utf-8", option = 1):
        if option == 1:
            try:
                opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(), urllib2.HTTPCookieProcessor())
                response = opener.open(url)
                html = response.read()
                content = html.decode(code, "ignore")
                return content
            except Exception, what:
                print what
                return None
        
        elif option == 2:
            try :
                driver = webdriver.Firefox()
                driver.get(url)
                content = driver.page_source
                driver.quit() 
                return content
            except Exception, what:
                print what
                return None

    def buildTree(self, content):
        try:
            tree = lxml.html.parse(StringIO.StringIO(content))
        except:
            return None
        return tree
        
    def getContent(self):
        return self.content
    
    def getTree(self):
        return self.tree
    
if __name__=='__main__':
    spider = Espider("http://www.amazon.cn/DQ-%E5%8D%95%E8%82%A9%E6%91%84%E5%BD%B1%E5%8C%85-%E5%8D%95%E5%8F%8D%E5%8C%85-%E5%8A%A0%E5%8E%9A%E5%8D%87%E7%BA%A7%E7%89%88/dp/B008MERV8K/ref=pd_rhf_dp_s_cp_1_RPK5")
    print spider.getContent()
