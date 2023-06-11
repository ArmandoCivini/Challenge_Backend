import xlsxwriter
from queries import get_all_countries
from data_insertion import insert_data


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


workbook = xlsxwriter.Workbook('challenge.xlsx')
worksheet = workbook.add_worksheet("Countries")

session = insert_data()

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

workbook.close()
