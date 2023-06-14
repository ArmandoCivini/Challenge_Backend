from database_schema import Country, CountryLanguage
from sqlalchemy.sql import functions, desc


def get_all_countries(session):
    return session.query(Country).all()


def get_top_10_population(session):
    countries = session.query(Country).order_by(
        Country.population.desc()).limit(10).all()
    names = [country.name for country in countries]
    populations = [country.population for country in countries]
    return names, populations


def get_area_percentage(session):
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
    language_rank = session.query(CountryLanguage.language_name,
                                  functions.
                                  count(CountryLanguage.language_name).label(
                                        "count")
                                  ).filter(
        CountryLanguage.order == 2).group_by(
        CountryLanguage.language_name).order_by(desc('count')).limit(1).all()
    return language_rank
