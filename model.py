from requests_html import AsyncHTMLSession
import asyncio
from bs4 import BeautifulSoup
import pandas as pd

class Data_Extractor:
   
    def __init__(self, url_without_params):
        self.asession = AsyncHTMLSession()
        self.url_without_params = url_without_params
        self.urls = []

    def generating_urls(self):
        for number in range(1,3):
            if number == 1:
                url = self.url_without_params
            else:
                url = self.url_without_params + f'?page={number}#search'
            self.urls.append(url)

    async def request(self,url):
        response = await self.asession.get(url)
        await response.html.arender(timeout = 10)
        response = response.html.raw_html
        return response

    def main(self):
        self.generating_urls()
        self.list_of_responses = self.asession.run(*[lambda url = url: self.request(url) for url in self.urls])
        
        
class Data_Cleaning(Data_Extraction):
    
    def __init__(self, data_extraction):
        self.list_of_responses = data_extraction.list_of_responses
        
    def __byte_to_bs4(self, byte_file):
        return BeautifulSoup(byte_file,'lxml')
    
    def parsing_data(self, index, lista):
        #We convert the byte object into a bs4 object
        content = self.__byte_to_bs4(self.list_of_responses[index])
        
        #We detect all the coins in the page
        all_coins = content.find('table').find('tbody').find_all('tr')
        
        #We extract each variable from them
        for coin in all_coins:
            money = coin.find('div',{'class':'ps--table__double'}).find_all('div')[1].text.replace('$','')
            participants = coin.find('td',{'data-project-finalized-target':'statsParticipantsCount'}).text
            total_raise = coin.find('td',{'data-project-finalized-target':'statsTotalRaise'}).text
            current_price = coin.find('td',{'data-project-finalized-target':'statsCurrentPrice'}).text
            ath = coin.find('td',{'data-project-finalized-target':'statsAth'}).text
            link = "https://polkastarter.com/projects/" + (coin.find('div',{'class':'ps--table__double'}).find_all('div')[0].text).lower().replace(' ', '-').replace('.','-')
            ido_date = coin.find('div',{'data-project-finalized-target':'statsFundedAtDate'}).text
            
            string = f"{money} -- {participants} -- {total_raise} -- {current_price} -- {ath} -- {link} -- {ido_date}"
            lista.append(string)
            
    def generating_dataframe(self, lista):
        df = pd.DataFrame({'content':listas})
        df = df['content'].str.split(' -- ', expand = True)
        self.df = df.rename({0:'money',
                        1:'participants',
                        2:'total_raise',
                        3:'current_price',
                        4:'ath',
                        5:'link',
                        6:'ido_date'
                        }, axis = 1)
        
    def returning_table(self):
        self.df.to_csv('polkastarter_analysis.csv')
