import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker


class PlotManager:
    def __init__(self):
        sns.set_theme(style="darkgrid")  # More visible grid
        sns.set_context("notebook", font_scale=1.2)  # Larger fonts
        sns.set_palette("deep")  # Deep color
        
        plt.rcParams['figure.figsize'] = [12, 8]
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['lines.linewidth'] = 2.5
        plt.rcParams['lines.markersize'] = 8
        
        self.years = sorted([str(i) for i in range(1970,2021, 10)] + [str(i) for i in range(2022,2024)])

    
    def takeMainInformation(self, dataFiltered, dataset, show=True):
        all_data = []
        for country in dataFiltered.index:
            try:
                for year in self.years:
                    data_point = {
                        'Year': int(year),
                        'Country': country
                    }
                    if ('population', year) in dataFiltered.columns:
                        population = dataFiltered.loc[country, ('population', year)]
                        if pd.notna(population):
                            data_point['Population'] = population
                    if ('co2_total', year) in dataFiltered.columns:
                        co2 = dataFiltered.loc[country, ('co2_total', year)]
                        if pd.notna(co2):
                            data_point['CO2 Total'] = co2        
                    if ('co2_per_capita', year) in dataFiltered.columns:
                        co2_per_capita = dataFiltered.loc[country, ('co2_per_capita', year)]
                        if pd.notna(co2_per_capita):
                            data_point['CO2 Per Capita'] = co2_per_capita
                    if ('birth_rate', year) in dataFiltered.columns:
                        birth_rate = dataFiltered.loc[country, ('birth_rate', year)]
                        if pd.notna(birth_rate):
                            data_point['Birth Rate'] = birth_rate
                            
                    if len(data_point) > 2:  # More than just Year and Country
                        all_data.append(data_point)
                        
            except Exception as e:
                print(f"Warning: Error processing {country}: {e}")
                continue
        return all_data

    def takeadditionalInformation(self, dataFiltered, dataset, show=True):
        all_data = []
        for country in dataFiltered.index:
            try:
                for year in self.years:
                    data_point = {
                        'Year': int(year),
                        'Country': country
                    }
                    if ('generation_GW', year) in dataFiltered.columns:
                        generation = dataFiltered.loc[country, ('generation_GW', year)]
                        if pd.notna(generation):
                            data_point['Electricity Generation (GW)'] = generation           
                    if ('consumption_GW', year) in dataFiltered.columns:
                        consumption = dataFiltered.loc[country, ('consumption_GW', year)]
                        if pd.notna(consumption):
                            data_point['Electricity Consumption (GW)'] = consumption
                    if len(data_point) > 2:  # More than just Year and Country
                        all_data.append(data_point)
                        
            except Exception as e:
                print(f"Warning: Error processing {country}: {e}")
                continue
        return all_data

    def plotlocal(self, dataset, countries, show=True):
        if not isinstance(countries, list):
            print("Error: countries must be a list")
            return None
            
        if len(countries) < 1:
            print("Error: Please provide at least one country")
            return None

        countries = [country.lower() for country in countries]
        dataset = dataset.copy()
        df_filtered = dataset.loc[countries]
        if df_filtered.empty:
            print("Error: None of the specified countries were found in the dataset")
            print("Available countries:", sorted(dataset['country'].unique()))
            return None

        all_data = self.takeMainInformation(df_filtered, dataset, show)
        additional_data = self.takeadditionalInformation(df_filtered, dataset, show)
        all_data.extend(additional_data)

        df = pd.DataFrame(all_data)
        if df.empty:
            print("Error: No data available to plot")
            return None
        self.plotCO2AndPopulation(df, countries, show)
        self.plotElectricityData(df, countries, show)
        plt.show()

    @staticmethod
    def millions_formatter(x, pos):
        return f'{x/1e6:.1f}M'

    def plotCO2AndPopulation(self, dataset, countries, show=True):
        sns.set_style("whitegrid", {'grid.linestyle': '--'})
        n_colors = len(countries)
        sns.color_palette("husl", n_colors)
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        
        sns.lineplot(data=dataset, x='Year', y='Population', hue='Country', 
            ax=ax1, marker='o')

        ax1.yaxis.set_major_formatter(ticker.FuncFormatter(self.millions_formatter))
        ax1.set_ylabel('Population')
        
        ax2 = ax1.twinx()
        sns.lineplot(data=dataset, x='Year', y='CO2 Total', hue='Country', 
                               ax=ax2, linestyle='--', marker='s')
        ax2.set_ylabel('CO2 Total')
        
        plt.title('Population et CO2 Total par Pays')
        legend_labels = []
        handles = []
        pop_handles = ax1.lines
        co2_handles = ax2.lines
        for i, country in enumerate(countries):
            legend_labels.extend([f'Population - {country}', f'CO2 Total - {country}'])
            handles.extend([pop_handles[i], co2_handles[i]])
        
        ax1.legend(handles, legend_labels, title='Métriques par Pays', 
                  bbox_to_anchor=(1.15, 1))
        ax2.get_legend().remove()
        fig1.tight_layout()
        
    def plotElectricityData(self, dataset, countries, show=True):
        fig2, ax3 = plt.subplots(figsize=(12, 6))
        
        sns.lineplot(data=dataset, x='Year', y='Electricity Generation (GW)', 
                    hue='Country', ax=ax3, marker='o')
        sns.lineplot(data=dataset, x='Year', y='Electricity Consumption (GW)', 
                    hue='Country', ax=ax3, linestyle='--', marker='s')
        
        plt.title('Génération et Consommation d\'Électricité par Pays')
        ax3.set_ylabel('GW')
        legend_labels = []
        for country in countries:
            legend_labels.extend([f'Generation - {country}', f'Consumption - {country}'])
            
        handles = ax3.lines[::2] + ax3.lines[1::2]
        ax3.legend(handles, legend_labels, title='Métriques par Pays', 
                  bbox_to_anchor=(1.15, 1))
        fig2.tight_layout()