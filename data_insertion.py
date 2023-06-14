from database_schema import (get_engine, Country,
                             CountryLanguage, Language,
                             Currency, CountryCurrency)
from sqlalchemy.orm import Session
from data_fetcher import get_countries_data


def get_attribute(obj, attr):
    if attr in obj:
        return obj[attr]
    else:
        return None


def get_attribute_indx(obj, attr, indx):
    if attr in obj:
        return obj[attr][indx]
    else:
        return None


def add_currencies(currencies_data, country, curr_dict):
    # adds all currencies of a country to the database
    if currencies_data is None or len(currencies_data) == 0:
        return country, curr_dict
    i = 1
    for code, currency_data in currencies_data.items():
        if code in curr_dict:
            currency = curr_dict[code]
        else:
            currency = Currency(code=code, name=currency_data["name"],
                                symbol=get_attribute(currency_data, "symbol"))
            curr_dict[code] = currency
        country_currency = CountryCurrency(order=i)
        country_currency.currency = currency
        country.currencies.append(country_currency)
        i += 1
    return country, curr_dict


def add_languages(languages_data, country, langs_dict):
    # adds all languages of a country to the database
    if languages_data is None or len(languages_data) == 0:
        return country, langs_dict
    i = 1
    for name in languages_data.values():
        if name in langs_dict:
            language = langs_dict[name]
        else:
            language = Language(name=name)
            langs_dict[name] = language
        country_language = CountryLanguage(order=i)
        country_language.language = language
        country.languages.append(country_language)
        i += 1
    return country, langs_dict


def add_country(country_data, session, langs_dict, curr_dict):
    # adds a country to the database
    name = country_data["name"]["common"]
    capital = get_attribute_indx(country_data, "capital", 0)
    currencies = get_attribute(country_data, "currencies")
    continent = country_data["continents"][0]
    Languages = get_attribute(country_data, "languages")
    population = country_data["population"]
    flag = country_data["flags"]["png"]
    area = country_data["area"]
    country = Country(name=name,
                      capital=capital,
                      continent=continent,
                      population=population,
                      flag=flag,
                      area=area
                      )
    country, curr_dict = add_currencies(currencies, country, curr_dict)
    country, langs_dict = add_languages(Languages, country, langs_dict)
    session.add(country)
    return langs_dict, curr_dict


def add_countries(data, session):
    # adds all countries to the database
    langs_dict = {}
    curr_dict = {}
    for country_data in data:
        langs_dict, curr_dict = add_country(country_data, session,
                                            langs_dict, curr_dict)
    session.commit()


def insert_data():
    engine = get_engine()
    session = Session(bind=engine)

    data = get_countries_data()
    add_countries(data, session)
    return session
