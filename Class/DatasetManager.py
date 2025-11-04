import pandas as pd
import os
import tkinter as tk
from tkinter import ttk
from pandastable import Table
from . import WebSiteFormater

class DatasetManager():
    def __init__(self, localPath="", websiteUrl= ""):
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
        if self.local_path == "" or self.local_path is None:
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
            return None
            
        root = tk.Tk()
        root.title("Local Dataset Viewer")
        root.geometry("800x600")
        
        frame = ttk.Frame(root)
        frame.pack(fill='both', expand=True)
        
        pt = Table(frame, dataframe=self.datasets["local"], showtoolbar=True, showstatusbar=True)
        pt.show()
        
        root.mainloop()
        
        return self.datasets["local"]
    
    def showWebDataset(self):
        if "local" not in self.datasets:
            print("Please init your dataset before")
            return None
        
        if "web" not in self.datasets:
            print("Web dataset not initialized")
            return None
            
        root = tk.Tk()
        root.title("Web Dataset Viewer")
        root.geometry("800x600")
        
        frame = ttk.Frame(root)
        frame.pack(fill='both', expand=True)
        
        pt = Table(frame, dataframe=self.datasets["web"], showtoolbar=True, showstatusbar=True)
        pt.show()
        
        root.mainloop()
        
        return self.datasets["web"]
    
    def showMergedDataset(self):
        if "local" not in self.datasets:
            print("Please init your dataset before")
            return None

        if "merged" not in self.datasets:
            print("Merged dataset not initialized")
            return None
            
        root = tk.Tk()
        root.title("Merge Dataset Viewer")
        root.geometry("800x600")
        
        frame = ttk.Frame(root)
        frame.pack(fill='both', expand=True)


        display_df = self.datasets["merged"].copy() # Create a copy of the merged dataset with the index as a column
        display_df.index.name = 'country'  # Name the index
        display_df = display_df.reset_index()  # Make index a column

        pt = Table(frame, dataframe=display_df, showtoolbar=True, showstatusbar=True)
        pt.show()
        
        root.mainloop()

        return self.datasets["merged"]
    
    def getAllCountries(self):
        if "local" not in self.datasets:
            print("Please init your dataset before")
            return None

        list_countries = [country.lower().replace(" ", "-") for country in self.datasets["local"]['country'].unique()]
        
        return list_countries
    
    def initWebDataset(self):
        if self.website_url == "" or self.website_url is None:
            self.website_url = input("insert the url to your dataset")
        
        webFormatter = WebSiteFormater.WebSiteFormater(self.website_url, self.getAllCountries())
        webDataset = webFormatter.getWebDataset()
        if webDataset.shape is not None:
            self.datasets["web"] = webDataset
        else:
            print("adding into dict failed")
        return 0
    
    def setStartupParameters(self):
        self.datasets['local']['country'] = self.datasets['local']['country'].str.lower()
        self.datasets['web']['country'] = self.datasets['web']['country'].str.lower()
        years = sorted([col.replace(" population", "") for col in self.datasets['local'].columns 
                        if "population" in col])
        metrics = ['population', 'co2_total', 'co2_per_capita', 'birth_rate', 
                    'fertility_rate', 'generation_GW', 'consumption_GW']
        countries = set(self.datasets['local']['country']) & set(self.datasets['web']['country'])
        return years, metrics, countries

    def createMergedDataFrame(self, merged_df):
        country_col = merged_df.pop('country') #remove coountry name value 
        merged_df.index = country_col #set country name value like index
        cols = [col for col in merged_df.columns if isinstance(col, tuple)]
        merged_df.columns = pd.MultiIndex.from_tuples(cols, names=['metric', 'year'])
        merged_df = merged_df.reindex(sorted(merged_df.columns), axis=1)
        self.datasets["merged"] = merged_df       
        return 0

    def mergeDatasets(self):
        if "local" not in self.datasets or "web" not in self.datasets:
            print("Please init both datasets before merging")
            return 1
        data = []
        years, metrics, countries = self.setStartupParameters()
        for country in countries:
            local_data = self.datasets['local'][self.datasets['local']['country'] == country] #use mask to return when the correct row
            web_data = self.datasets['web'][self.datasets['web']['country'] == country]
            if not local_data.empty and not web_data.empty:
                row_data = {'country': country}
                if 'area (km²)' in local_data:
                    area = local_data['area (km²)'].iloc[0]
                row_data[('area (km²)', '')] = area
                for year in years:
                    pop_col = f"{year} population"
                    if pop_col in local_data.columns:
                        row_data[('population', year)] = local_data[pop_col].iloc[0]
                    
                    for metric in metrics[1:]:
                        col_name = f"{metric}_{year}"
                        if col_name in web_data.columns:
                            row_data[(metric, year)] = web_data[col_name].iloc[0]
                data.append(row_data)
        
        merged_df = pd.DataFrame(data)
        if merged_df.empty:
            print("\nERROR: Merge resulted in empty dataset!")
            return 1
        self.createMergedDataFrame(merged_df)
        return 0
    

