
#!/usr/bin/env python3

import sys
import DatasetManager
import PlotManager

def print_available_countries(dataset):
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

def select_countries(dataset):
    available_countries = print_available_countries(dataset)
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

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 Interface.py <local_dataset_path> <website_url>")
        return 84

    local_dataset_path = sys.argv[1]
    website_url = sys.argv[2]

    datasetManager = DatasetManager.DatasetManager(websiteUrl=website_url, localPath=local_dataset_path)
    plotManager = PlotManager.PlotManager()

    if datasetManager.initialize_local_dataset() != 0:
        print("Local dataset initialization failed.")
        return 84

    if datasetManager.initWebDataset() != 0:
        print("Web dataset initialization failed.")
        return 84

    datasetManager.mergeDatasets()

    selected_countries = select_countries(datasetManager.datasets["merged"])
    
    if not selected_countries:
        print("No countries selected.")
        return 84
    
    plotManager.plotlocal(datasetManager.datasets["merged"], selected_countries)

    return 0


if __name__ == "__main__":
    sys.exit(main())
    main()
