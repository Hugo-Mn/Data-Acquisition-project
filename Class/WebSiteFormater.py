import urllib.request
import pandas as pd
import beautifulsoup4 as bs4



class WebSiteFormater:
    
    def __init__(self, url, countries):
        self.url = url
        self.countries = countries
        self.years = [str(i) for i in range(1970,2023, 10)]
        self.colNames = ["co2_total", "co2_per_capita", "birth_rate", "fertility_rate", "generation_GW", "consumption_GW"]
        self.lst_Info = ["energy-and-environment/co2-emissions/", "demography/fertility/", "energy-and-environment/electricity-consumption/"]
        self.lst_Info_Value = {}
        self.webDataSet = None
    
    def format_url(self, info, country):
        formatted_url = self.url
        formatted_url = formatted_url.replace("{info}", info)
        formatted_url = formatted_url.replace("{country}", country)
        return formatted_url

    def openUrl(self, url):
        try:
            response = urllib.request.urlopen(url)
            webContent = response.read()
            soup = bs4.BeautifulSoup(webContent, 'html.parser')
            return soup
        except:
            print(f"Opening url {url} failed")
            return None
        
    def foundInformation(self, id, website):
        infos = []
        allInformation = website.find("tr", {"id": id})
        if allInformation is None:
            return None
        for i in allInformation.find_all("td"):
            if i[0].text in self.years:
                take = self.takeInfomation(i, id)
                infos.append(take)
        return infos
    
    def takeInfomation(self, lstTd, id):
        tdlist = lstTd.find_all("td", class_="numero")
        value = []

        for i in range(len(tdlist)):
            if (id == 0 and i == 1) or (id != 0 and i == 2):
                continue
            value.append(float(tdlist[i].text.strip()))
        return value

    def getAllInformation(self):
        for country in self.countries:
            country_info = []
            for i in range(len(self.lst_Info)):
                url = self.format_url(self.lst_Info[i], country)
                website = self.openUrl(url)
                if website is None:
                    print(f"Opening website for country {country} and info {self.lst_Info[i]} failed")
                    return 84
                info = self.foundInformation(i, website)
                if info is None:
                    print(f"Finding information for country {country} and info {self.lst_Info[i]} failed")
                    return 84
                info = [j for i in info for j in i]
                country_info.append(info)
            self.lst_Info_Value[country] = country_info
        return 0
    
    def TransformToDataFrame(self):
        allInfo = self.getAllInformation()
        rows = []

        if allInfo != 0:
            return None

        for country, infos in self.lst_Info_Value.items():
            if infos is None:
                infos = []
            if len(infos) < len(self.colNames):
                infos += [None] * (len(self.colNames) - len(infos))
            rows.append([country] + infos)

        df = pd.DataFrame(rows, columns=["country"] + self.colNames)
        self.webDataSet = df

    def getWebDataset(self):
        if self.webDataSet is None:
            self.TransformToDataFrame()
        return self.webDataSet