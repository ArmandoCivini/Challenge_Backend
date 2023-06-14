import xlsxwriter
from queries import (get_all_countries, get_top_10_population,
                     get_area_percentage, get_most_common_second_language)
from data_insertion import insert_data
import seaborn as sns
import matplotlib.pyplot as plt


def set_attributes(attributes):
    if attributes is None:
        return -1
    for i, attribute in enumerate(attributes):
        if attribute.order == 1:
            return i
    return -1


def set_currency(country):
    num = set_attributes(country.currencies)
    if num == -1:
        country._currency = ""
        return country
    country._currency = country.currencies[num].currency.name
    return country


def set_language(country):
    num = set_attributes(country.languages)
    if num == -1:
        country._language = ""
        return country
    country._language = country.languages[num].language.name
    return country


def create_countries_sheet(workbook, session):
    worksheet = workbook.add_worksheet("Countries")

    countries = get_all_countries(session)

    worksheet.write(0, 0, "Name")
    worksheet.write(0, 1, "Capital")
    worksheet.write(0, 2, "Currencies")
    worksheet.write(0, 3, "Continent")
    worksheet.write(0, 4, "Languages")
    worksheet.write(0, 5, "Population")
    worksheet.write(0, 6, "Flag")

    for i, country in enumerate(countries):
        country = set_currency(country)
        country = set_language(country)

        worksheet.write(i+1, 0, country.name)
        worksheet.write(i+1, 1, country.capital)
        worksheet.write(i+1, 2, country._currency)
        worksheet.write(i+1, 3, country.continent)
        worksheet.write(i+1, 4, country._language)
        worksheet.write(i+1, 5, country.population)
        worksheet.write(i+1, 6, country.flag)


def add_top_10_population(worksheet, session):
    names, populations = get_top_10_population(session)

    fig = sns.barplot(x=names, y=populations)
    fig.set_ylabel("Population")
    fig.set_xlabel("Country")
    fig.set_title("Top 10 countries by population")
    fig.figure.set_size_inches(15, 10)
    fig.get_figure().savefig("top_10_countries.png")
    size_options = {'x_scale': 0.5, 'y_scale': 0.5}

    worksheet.insert_image(0, 0, "top_10_countries.png", size_options)


def add_area_percentage(worksheet, session):
    plt.clf()
    top_area_names, top_area_area = get_area_percentage(session)

    plt.pie(top_area_area, labels=top_area_names, autopct='%1.1f%%')
    plt.title("Area share by country")
    plt.savefig("area_share.png")
    size_options = {'x_scale': 0.5, 'y_scale': 0.5}

    worksheet.insert_image(0, 15, "area_share.png", size_options)


def add_most_common_second_language(worksheet, session):
    language_rank = get_most_common_second_language(session)
    worksheet.write(26, 0, "Most common second language:")
    worksheet.write(27, 0, "Language")
    worksheet.write(27, 1, "Count")
    worksheet.write(28, 0, language_rank[0][0])
    worksheet.write(28, 1, language_rank[0][1])


workbook = xlsxwriter.Workbook('challenge.xlsx')
worksheet = workbook.add_worksheet("Stats")

session = insert_data()
add_top_10_population(worksheet, session)
add_area_percentage(worksheet, session)
add_most_common_second_language(worksheet, session)


workbook.close()
