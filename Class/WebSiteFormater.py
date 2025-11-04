import sys
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm




class WebSiteFormater:
    
    def __init__(self, url, countries):
        self.url = url
        self.countries = countries
        self.years = sorted([str(i) for i in range(1970,2021, 10)] + [str(i) for i in range(2022,2024)], reverse=True)
        self.colNames = ["co2_total", "co2_per_capita", "birth_rate", "fertility_rate", "generation_GW", "consumption_GW"]
        self.lst_Info = ["energy-and-environment/co2-emissions/", "demography/fertility/", "energy-and-environment/electricity-consumption/"]
        self.lst_Info_Value = {}
        self.webDataSet = None
        self.keyweb = None
    
    def format_url(self, info, country):
        formatted_url = self.url
        formatted_url = formatted_url.replace("{info}", info)
        formatted_url = formatted_url.replace("{country}", country)
        return formatted_url

    def openUrl(self, url):
        try:
            self.keyweb = urllib.request.urlopen(url)
            webContent = self.keyweb.read()
            soup = BeautifulSoup(webContent, 'html.parser')
            return soup
        except:
            return None
        
    def foundInformation(self, id, website):
        infos = []
        allInformation = website.find_all("tbody")
        allInformation = allInformation[0].find_all("tr")
        if allInformation is None:
            return None
        for i in allInformation:
            line = i.find_all("td")
            if line[0].text in self.years:
                take = self.takeInfomation(line, id)
                infos.append(take)
        return infos
    
    def takeInfomation(self, lstTd, id):
        value = []
        lstTd = lstTd[1:]
        for i in range(len(lstTd)):
            if (id == 0 and i == 1) or (id != 0 and i == 2):
                continue
            if len(lstTd) > 3 and (i == 0 or i == 1 or i == 2):
                value.append(self.parseFloat(i , lstTd, False))
            elif len(lstTd) <= 3:
                value.append(self.parseFloat(i, lstTd, True))
            else:
                continue
        return value
    
    def parseFloat(self, id , lstTd, typeParse):
        if not typeParse:
            id = -(id + 1)
            if lstTd[id].text.strip() != '' and lstTd[id].text.strip() != None:
                return float(lstTd[id].text.strip().replace(",", "").replace("‰", ""))
            else:
                return None
        else:
            if lstTd[id].text.strip() != '' and lstTd[id].text.strip() != None:
                return float(lstTd[id].text.strip().replace(",", "").replace("‰", ""))
            else:
                return None

    def showError(self, error):
        for key, value in error.items():
            print (f"Error for {key}:")
            for v in value:
                print(f" - {v}")

    def getAllInformation(self):
        error = {}
        progress_bar = tqdm(self.countries, desc="Scraping Website")
        for country in progress_bar:
            progress_bar.set_description(f"Scraping Website: Processing {country}")
            country_info = []
            for i in range(len(self.lst_Info)):
                url = self.format_url(self.lst_Info[i], country)
                website = self.openUrl(url)
                if website is None:
                    error[self.lst_Info[i]] = error.get(self.lst_Info[i], []) + [country]
                    continue
                info = self.foundInformation(i, website)
                if info is None:
                    error["url"] = error.get("url", []) + [url]
                    continue
                if len(info) !=  len(self.years):
                    for i in range(len(self.years) - len(info)):
                        info.append([None, None])
                country_info.append(info)
            self.lst_Info_Value[country] = country_info
        self.showError(error)
        return 0
    
    def TransformToDataFrame(self):
        allInfo = self.getAllInformation()
        if allInfo != 0:
            return None

        categories = ['co2_total', 'co2_per_capita', 'birth_rate', 'fertility_rate', 'generation_GW', 'consumption_GW']
        
        data = []
        for country, country_data in self.lst_Info_Value.items():
            row = {'country': country}
            
            for id_category, category in enumerate(country_data):
                if category:
                    start_categories = id_category * 2
                    category_categories = categories[start_categories:start_categories + 2]
                    for id_year, year in enumerate(self.years):
                        if id_year < len(category):
                            year_values = category[id_year]
                            for id_subcategory, subcategory in enumerate(category_categories):
                                if id_subcategory < len(year_values):
                                    col_name = f"{subcategory}_{year}"
                                    row[col_name] = year_values[id_subcategory]

            data.append(row)
        df = pd.DataFrame(data)

        columns = ['country']
        for category in categories:
            for year in self.years:
                columns.append(f"{category}_{year}")

        df = df[columns]
        
        self.webDataSet = df

    def getWebDataset(self):
        if self.webDataSet is None:
            self.TransformToDataFrame()
            self.keyweb.close()
        return self.webDataSet