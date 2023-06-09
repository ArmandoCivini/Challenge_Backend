from data_fetcher import get_countries_data


data = get_countries_data()
for country in data:
    if "languages" not in country.keys():
        continue
    if len(country["languages"]) > 1:
        print(country["languages"])