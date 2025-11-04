# Data-Acquisition-project

# Dataset

This project aims to merge two datasets: one from a CSV file and another from web scraping.

## 1. Main Dataset
*[world_population_data.csv](https://www.kaggle.com/datasets/sazidthe1/world-population-data)*

This dataset contains demographic information for 234 countries from 1970 to 2023.

### Main Dataset Structure (CSV)

| Column           | Description                              |
|-----------------|------------------------------------------|
| rank            | Country ranking by population            |
| cca3            | Three-letter country code               |
| country         | Country name                            |
| continent       | Continent name                          |
| 2023 population | Population in 2023                      |
| 2022 population | Population in 2022                      |
| 2020 population | Population in 2020                      |
| 2015 population | Population in 2015                      |
| 2010 population | Population in 2010                      |
| 2000 population | Population in 2000                      |
| 1990 population | Population in 1990                      |
| 1980 population | Population in 1980                      |
| 1970 population | Population in 1970                      |
| area (km²)      | Country area in square kilometers       |
| density (km²)   | Population density (people per km²)     |
| growth rate     | Population growth rate                  |
| world percentage| Percentage of world population          |


## 2. Web Data

Source: [countryeconomy.com](https://countryeconomy.com)

The website provides comprehensive data about countries, including CO2 emissions, demographic information, and energy consumption metrics.

Data categories and their paths:

| Category | Path | Description |
|----------|------|-------------|
| CO2 emissions (total and per capita) | `energy-and-environment/co2-emissions/` | Total and per capita CO2 emissions data by country |
| Birth and fertility rates | `demography/fertility/` | Birth rates and fertility statistics |
| Electricity metrics | `energy-and-environment/electricity-consumption/` | Generation and consumption of electricity |

Note: Data is collected for each year matching the main dataset's timeframe (1970-2023)

### Web Data Structure

| Column            | Description                                  |
|-------------------|----------------------------------------------|
| country           | Country name                                 |
| year              | Data collection year                         |
| co2_total         | Total CO2 emissions for the country          |
| co2_per_capita    | CO2 emissions per person                     |
| birth_rate        | Number of births per 1000 population         |
| generation_GW     | Total electricity generation in gigawatts    |
| consumption_GW    | Total electricity consumption in gigawatts   |

## 3. Combined Dataset Structure

This dataset merges key information from both sources to analyze the relationship between population growth, CO2 emissions, and energy consumption. It enables the study of potential correlations between demographic changes and environmental impacts across different countries and years.

```markdown
| country | year | population | co2_total | co2_per_capita | birth_rate | generation_GW | consumption_GW |
|---------|------|------------|-----------|----------------|------------|---------------|----------------|
| france  | 1970 | xxx        | xxx       | xxx           | xxx        | xxx           | xxx           |
| germany | 1970 | xxx        | xxx       | xxx           | xxx        | xxx           | xxx           |
| ...     |      |            |           |               |            |               |               |
```

### Available Metrics

- **Population**: Total number of inhabitants in the country
- **CO2 Total**: Total CO2 emissions for the country (in metric tons)
- **CO2 per Capita**: CO2 emissions per person (in metric tons)
- **Birth Rate**: Number of births per 1000 population
- **Electricity Generation**: Total electricity production in gigawatts (GW)
- **Electricity Consumption**: Total electricity consumption in gigawatts (GW)

## 4. Visualization

### Growing Population and CO2 Emissions

If you have plotted some graphs and compared a few countries, you have already noticed that the growing population is not a really influential factor in the emissions of CO2. The best example possible is to plot a graph with *Germany*, *Bulgaria* and *Zambia*:

You can see for *Bulgaria* when the population number and the CO2 emissions stay close to each other across time, the simple observation could be to say that population is the main influence in CO2 Emissions... but observe the plots for *Germany* and *Zambia*: you can see that *Germany's* emissions still decrease but its population grows, and for *Zambia* it's more remarkable because the CO2 emissions stay the same but the population grows across time...

So you can observe this for every country in the world, the main factor in CO2 emissions is not the population but maybe the laws and how the governments fight against it.

### Generation and Consumption Electricity

For electricity data analysis, we examine both generation and consumption patterns across different countries and their correlation with population and economic development. Some countries like *France* show interesting patterns where electricity generation doesn't increase even as population and consumption rise. This suggests there is a strong correlation between consumption and population growth, but not necessarily between population and electricity generation.

## ChatGPT Prompts and Responses

### Prompt 1: Grammar Correction

**Question:** Fix grammar in the text while keeping the same meaning

**Response:**
The text was corrected while maintaining its original meaning and analysis of the relationship between population and CO2 emissions.

### Prompt 2: Dataset Structure

**Question:** Create a table structure for the main dataset columns

**Response:**

| Column           | Description                              |
|-----------------|------------------------------------------|
| rank            | Country ranking by population            |
| cca3            | Three-letter country code               |
| country         | Country name                            |
| continent       | Continent name                          |
| 2023 population | Population in 2023                      |
| 2022 population | Population in 2022                      |
| 2020 population | Population in 2020                      |
| 2015 population | Population in 2015                      |
| 2010 population | Population in 2010                      |
| 2000 population | Population in 2000                      |
| 1990 population | Population in 1990                      |
| 1980 population | Population in 1980                      |
| 1970 population | Population in 1970                      |
| area (km²)      | Country area in square kilometers       |
| density (km²)   | Population density (people per km²)     |
| growth rate     | Population growth rate                  |
| world percentage| Percentage of world population          |

### Prompt 3: Axis Formatting

**Question:** How to format axis values in millions instead of using scientific notation?

**Response:**

Function to format axis values in millions:

```python
@staticmethod
def millions_formatter(x, pos):
    return f'{x/1e6:.1f}M'
```

Implementation in the plot:

```python
sns.lineplot(data=dataset, x='Year', y='Population', hue='Country', ax=ax1, marker='o')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(self.millions_formatter))
ax1.set_ylabel('Population (Millions)')
```

### Prompt 4: Check Readme

**Question:** Check if the readme is Okay and fix syntax if you need

**Response:**

I have reviewed and improved the README file. Here are the changes made:

1. Document Structure:
   - Added proper section spacing
   - Fixed table formatting and alignment
   - Improved overall document organization

2. Content Improvements:
   - Fixed grammar and spelling in all sections
   - Enhanced the "Generation and Consumption Electricity" section
   - Added detailed descriptions for data relationships

3. Formatting Enhancements:
   - Standardized Markdown syntax
   - Improved heading hierarchy
   - Added consistent code block formatting
   - Fixed list indentation and spacing

4. Documentation Quality:
   - Ensured clear and professional language
   - Maintained consistent style throughout
   - Added proper technical terminology

The document now follows best practices for technical documentation and provides a clear overview of the project structure and findings.
