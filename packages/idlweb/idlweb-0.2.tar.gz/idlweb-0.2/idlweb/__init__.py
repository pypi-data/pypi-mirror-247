import requests
from bs4 import BeautifulSoup
import urllib.request 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
none=None 
class _forms:
    def formlog(html,num=0):
        forms_name={}
        htmlparser=BeautifulSoup(html,'html.parser')
        try:
            forms=htmlparser.find_all('form')[0]
        except:
            raise TypeError('Error list index out of range')
        all_name = [
            name.get('name') for name in forms.find_all(attrs={"name":True})
        ]
        all_tga = [
            name for name in forms.find_all(attrs={"name":True})
        ]
        for name in all_name:
            tag = forms.find(attrs={'name':name})
            value = tag.get('value')
            forms_name[name]=value if value else "" 
        return forms_name , forms
    def ActionRrl(from_action,url,format_url,_parse):
        action = from_action.get('action')
        if action:
            action=action.strip()  
            base = _parse.UrlParse(action)
            if base:
                return action 
            else:
                if action[:1] == "/":
                    return format_url+action 
                if action[:1] != "/":
                    return format_url+"/"+action 
        return url 
class _urlparse:
    def UrlParse(url):
        if 'http://' in url or 'https://' in url:
            if url.startswith('http://'):
                    protocol = "http://"
                    host=url[7:]
            if url.startswith('https://'):
                protocol = "https://"
                host=url[8:]
            if '/' in host:
                host=host.split('/')[0]
            new_u=protocol+host
            return new_u
        return False 
class Browser:
    def __init__(self) -> None:
        self.root_session = requests.Session()
        self.url=none 
        self.response = none 
        self.headers = {} 
        self.proxy = {} 
        self.format_url = none 
        self.base_url = none 
        self.__form={}
        self.formhtml=none
        self.__action=none
    def useheaders(self,headers={}):
        self.headers = headers 
    def useproxy(self,proxy={}):
        self.proxy = proxy 
    def open(self,url):
        self.url=url
        self.response = self.root_session.get(url=url,headers=self.headers,proxies=self.proxy)
        self.format_url = _urlparse.UrlParse(self.url)  
    def select_form(self,num=0):
        self.__form,self.formhtml=_forms.formlog(html=self.response.text,num=num)
        self.data=self.__form
        self.__action=_forms.ActionRrl(from_action=self.formhtml,url=self.url,format_url=self.format_url,_parse=_urlparse)
    def set_form(self,key,value):
        if key in self.__form:
            self.__form[key]=value 
        else:
            raise ValueError(f"Error '{key}' not found in the form")
    def forms(self):
        for i in self.__form:
            val=f"'{i}':'{self.__form[i]}'"
            yield val 
    def formjson(self):
        return self.__form 
    def submit(self):
        return self.root_session.post(
            url=self.__action,
            headers=self.headers,
            data=self.__form
        )