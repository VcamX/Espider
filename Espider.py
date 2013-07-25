# -*- coding: utf-8 -*-
# hello world
import lxml.html
import urllib2
import gzip
import zlib
import cookielib
import selenium

from StringIO import StringIO
        
class ContentEncodingProcessor(urllib2.BaseHandler):
    """
    A handler to add gzip or deflate capabilities to urllib2 requests
    """
    
    # add headers to requests
    def http_request(self, req):
        req.add_header("Accept-Encoding", "gzip, deflate")
        return req
    
    # method for deflate
    def deflate(self, data):   # zlib only provides the zlib compress format, not the deflate format;
        try:               # so on top of all there's this workaround:
            return zlib.decompress(data, -zlib.MAX_WBITS)
        except zlib.error:
            return zlib.decompress(data)
    
    # decode
    def http_response(self, req, resp):
        old_resp = resp
        # gzip
        if resp.headers.get("content-encoding") == "gzip":
            gz = gzip.GzipFile(
                    fileobj = StringIO(resp.read()),
                    mode = "r"
                )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
            resp.msg = old_resp.msg
    
        # deflate
        if resp.headers.get("content-encoding") == "deflate":
            gz = StringIO( self.deflate(resp.read()) )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
            resp.msg = old_resp.msg
        return resp
    
class Espider():
    def __init__(self, url, code = "utf-8", option = 1):
        self.url = url
        self.content = self.fetchContent(url, code, option)
        self.tree = self.buildTree(self.content)
        
    def fetchContent_raw(self, url = None, option = 1):
        if url == None: url = self.url
        #print url
        
        if option == 1:
            try:
                proxy = {"http": "http://"+"58.215.75.170:80"}
                #proxy = {}
                proxy_support = urllib2.ProxyHandler(proxy)
                opener = urllib2.build_opener(proxy_support, ContentEncodingProcessor, urllib2.HTTPCookieProcessor)
                webpage = opener.open(url)
                html = webpage.read()
                webpage.close()
                return html
                
            except Exception, what:
                print what
                return None
            
        elif option == 2:
            try :
                driver = selenium.webdriver.Firefox()
                driver.get(url)
                html = driver.page_source
                driver.quit()
                return html
            except Exception, what:
                print what
                return None
    
    def fetchContent(self, url, code = "utf-8", option = 1):
        html = self.fetchContent_raw(url, option)

        if html == None:
            return None
        else:
            if option == 1:
                content = html.decode(code, "ignore")
            else:
                content = html
            return content

    def buildTree(self, content):
        try:
            tree = lxml.html.parse(StringIO(content))
        except:
            return None
        return tree
        
    def getContent(self):
        return self.content
    
    def getTree(self):
        return self.tree
    
if __name__=='__main__':
    import chardet
    
    url = "http://www.360buy.com/product/783200.html"
    #url = "http://www.huihui.cn/hui/9291499/redirect"
    spider = Espider(url, option = 1, code = "gb2312")
    
    html = spider.getContent()
    if html is not None:
        import chardet
        print chardet.detect(html)
        with open("1.html", "w") as f:
            f.write(html.encode("gb2312"))
