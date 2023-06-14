from database_schema import (Country, CountryLanguage,
                             CountryCurrency, Currency)
from sqlalchemy.sql import functions, desc


def get_all_countries(session):
    return session.query(Country).all()


def get_top_10_population(session):
    # returns the top 10 countries by population
    countries = session.query(Country).order_by(
        Country.population.desc()).limit(10).all()
    names = [country.name for country in countries]
    populations = [country.population for country in countries]
    return names, populations


def get_area_percentage(session):
    # returns the percentage of the world area of the top 9 countries
    # and accumulate the rest of the world in the 10th place
    total_area = session.query(functions.sum(Country.area)).scalar()
    top_area = session.query(Country).order_by(
        Country.area.desc()).limit(9).all()
    top_area_names = [country.name for country in top_area]
    top_area_area = [country.area for country in top_area]
    cum_area_top = sum(top_area_area)
    other = total_area - cum_area_top
    top_area_names.append("Other")
    top_area_area.append(other)
    return top_area_names, top_area_area


def get_most_common_second_language(session):
    # returns the most common second language out of all countries
    language_rank = session.query(CountryLanguage.language_name,
                                  functions.
                                  count(CountryLanguage.language_name).label(
                                        "count")
                                  ).filter(
        CountryLanguage.order == 2).group_by(
        CountryLanguage.language_name).order_by(desc('count')).limit(1).all()
    return language_rank


def get_most_common_currency(session):
    # returns the most common currency out of all countries
    currency_rank = session.query(CountryCurrency.currency_code,
                                  functions.
                                  count(CountryCurrency.currency_code).label(
                                        "count")
                                  ).group_by(
        CountryCurrency.currency_code).order_by(desc('count')).limit(1).all()
    currency_name = session.query(Currency.name).filter(
        Currency.code == currency_rank[0][0]).all()
    return currency_name[0][0], currency_rank[0][1]


def get_countries_density(session):
    # returns the population, area and continent of all countries
    density = session.query(
        Country.population, Country.area, Country.continent).all()
    population = [country[0] for country in density]
    area = [country[1] for country in density]
    continent = [country[2] for country in density]
    density_dict = {"population": population, "area": area,
                    "continent": continent}
    return density_dict
