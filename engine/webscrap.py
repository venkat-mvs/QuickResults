# -*- coidng:utf-8 -*-
import requests
from sys import exit
from bs4 import BeautifulSoup
import abc

class BaseWebScrapper(abc.ABC):
    @abc.abstractmethod
    def get_results(self,url,form):
        # should return following format
        #return {"header":__,"marks":__,"credits":__,"sgpa":__} 
        pass

class MarksWebScraper(BaseWebScrapper):
    def __init__(self,url):
        self.url = url
    def get_results(self,form):
        url = self.url
        try:
            response = requests.post(url,form)
        except:
            print("Network Connection required"
                " May be your network is slow")
            exit(1)

        html = BeautifulSoup(response.text,"html.parser")
        
        title = html.find('div',{'id':'title'}).text
        #print(title)
        credits,sgpa = html.find_all('table',{'class':'tborder'})[1].find_all('td')
        credits,sgpa = credits.find('b').text,sgpa.find('b').text

        try:
            trs = [i for i in html.find("table",{"class":"dtlsbdr"}).children][:]
        except:
            print("Looks like your roll number is wrong")
            return None
        def recursive_tag_extractor(tag):
            tag = tag.find(tag.name)
            if tag==None:
                return
            else:
                trs.append(tag)
                recursive_tag_extractor(tag)
        recursive_tag_extractor(trs[1])

        marks = []
        for tr in trs:
            subject = []
            for td in tr.children:
                if td.name != "tr":
                    subject.append(td.text)
            marks.append(subject)
            
        return {"header":marks[0],"marks":marks[1:],"credits":credits,"sgpa":sgpa,'title':title} 



if __name__ == '__main__': 
    url = "http://www.nriitexamcell.com/autonomous/results/2-1-nov-2019.php"
    obj = MarksWebScraper(url)
    roll = '18kn1a0538' #input("Enter your roll number : ")
    form = {"roll":roll,"submit":"Submit"}
    print(obj.get_results(form))

