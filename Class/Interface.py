from . import DatasetManager
from . import PlotManager


class Interface:
    def __init__(self):
        self.local_path = "./Dataset/world_population_data.csv"
        self.website_url = "https://countryeconomy.com/{info}/{country}"
        self.DatasetManager = DatasetManager.DatasetManager(localPath=self.local_path, websiteUrl=self.website_url)
        self.PlotManager = PlotManager.PlotManager()
    
    def print_available_countries(self, dataset):
        print("\nCountries list available:")
        available_countries = sorted(dataset.index.unique())
        
        max_len = max(len(f"{i}. {country.capitalize()}") for i, country in enumerate(available_countries, 1))
        col_width = max_len + 4
        
        n_countries = len(available_countries)
        n_rows = (n_countries + 2) // 5
        
        for row in range(n_rows):
            line = ""
            for col in range(5):
                idx = row + col * n_rows
                if idx < n_countries:
                    country = available_countries[idx]
                    item = f"{idx + 1}. {country.capitalize()}"
                    line += item.ljust(col_width)
            print(line.rstrip())
        return available_countries

    def select_countries(self, dataset):
        available_countries = self.print_available_countries(dataset)
        selected_countries = []
        
        while len(selected_countries) < 5:
            print(f"\nSelect a country (1-{len(available_countries)}) or type 'done' to finish:")
            choice = input("> ").strip().lower()
            
            if choice == 'done':
                if len(selected_countries) == 0:
                    print("Please select at least one country.")
                    continue
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(available_countries):
                    country = available_countries[index]
                    if country in selected_countries:
                        print(f"{country.capitalize()} is already selected.")
                    else:
                        selected_countries.append(country)
                        print(f"{country.capitalize()} added. {len(selected_countries)}/5 countries selected.")
                        if len(selected_countries) == 5:
                            print("Maximum number of countries reached (5).")
                            break
                else:
                    print("Invalid choice. Please select a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number or 'done' to end.")

        print("\nSelected countries:")
        for country in selected_countries:
            print(f"- {country.capitalize()}")
        
        return selected_countries

    def main_loop(self, datasetManager, plotManager):
        exit = False
        while not exit:
            print("\nMenu :")
            print("1. (s)elect countries to plot")
            print("2. (e)xit")
            choice = input("> ").strip()
            if choice == '1' or choice.lower().startswith('s'):
                selected_countries = self.select_countries(datasetManager.datasets["merged"])
                if selected_countries:
                    plotManager.plotlocal(datasetManager.datasets["merged"], selected_countries)
                else:
                    print("No countries selected.")
            elif choice == '2' or choice.lower().startswith('e'):
                print("Exiting...")
                exit = True
            else:
                print("Invalid choice. Please select 1 or 2.")

    def init_Managers(self):
        print("Initializing Dataset Manager...")
        print("Loading local dataset...")
        if self.DatasetManager.initialize_local_dataset() != 0:
            print("Local dataset initialization failed.")
            return None
        else:
            print("Local dataset initialized successfully.")

        if self.DatasetManager.initWebDataset() != 0:
            print("Web dataset initialization failed.")
            return None
        else:
            print("Web dataset initialized successfully.")
        print("Merging datasets...")
        self.DatasetManager.mergeDatasets()
        print("Datasets merged successfully.")

    def run_interface(self):
        self.init_Managers()
        self.main_loop(self.DatasetManager, self.PlotManager)
        return 0

