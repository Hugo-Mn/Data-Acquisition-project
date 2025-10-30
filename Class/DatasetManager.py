import pandas as pd
import WebSiteFormater
import os

class DatasetManager():
    def __init__(self, websiteUrl= "",localPath="" ):
        self.datasets = {}
        self.website_url = websiteUrl
        self.local_path = localPath
    
    def set_local_path(self, path):
        self.local_path = path
        print(f"set local path to : {path}")

    def set_website_url(self, url):
        self.website_url = url
        print(f"set website url to : {url}")

    def initialize_local_dataset(self, delimiter=','):
        if self.local_path is "" or self.local_path is None:
            self.local_path = input(f"actual folder {os.getcwd()} insert the path to your dataset")
        try:

            dataset = pd.read_csv(self.local_path)
            if dataset.shape is not None:
                self.datasets["local"] = dataset
            else:
                print("adding into dict failed")
            return 0
        except:
            print(f"Reading dataset failed ")
            return 84
    
    def showLocalDataset(self):
        if "local" not in self.datasets:
            print("Please init your dataset before")
            return 1
        self.datasets["local"].head()
        return 0
    
    def getAllCountries(self):
        if "local" not in self.datasets:
            print("Please init your dataset before")
            return None
        list_countries = self.datasets["local"]['Country'].unique()
        for i in list_countries:
            i = i.lower().replace(" ", "-")
        return list_countries
    
    def initWebDataset(self):
        if self.website_url is "" or self.website_url is None:
            self.website_url = input("insert the url to your dataset")
        try:
            webFormatter = WebSiteFormater.WebSiteFormater(self.website_url, self.getAllCountries())
            webDataset = webFormatter.getWebDataset()
            if webDataset.shape is not None:
                self.datasets["web"] = webDataset
            else:
                print("adding into dict failed")
            return 0
        except:
            print(f"Reading dataset from web failed ")
            return 84
    def showWebDataset(self):
        if "web" not in self.datasets:
            print("Please init your dataset before")
            return 1
        self.datasets["web"].head()
        return 0
    
    def mergeDatasets(self,):
        if "local" not in self.datasets or "web" not in self.datasets:
            print("Please init both datasets before merging")
            return 1
        merged_dataset = pd.merge(self.datasets["local"], self.datasets["web"], on="country", how="inner")
        self.datasets["merged"] = merged_dataset
        return 0

