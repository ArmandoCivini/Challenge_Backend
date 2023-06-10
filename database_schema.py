from sqlalchemy import (create_engine, Column,
                        Integer, String, ForeignKey
                        )
from sqlalchemy.orm import declarative_base, relationship

# Make the engine
engine = create_engine("sqlite+pysqlite:///:memory:", future=True, echo=False)

# Make the DeclarativeMeta
Base = declarative_base()


class Country(Base):
    __tablename__ = "countries_table"

    name = Column(String, primary_key=True)
    capital = Column(String)
    currencies = relationship("CountryCurrency", back_populates="country")
    continent = Column(String)
    languages = relationship("CountryLanguage", back_populates="country")
    population = Column(Integer)
    flag = Column(String)
    area = Column(Integer)


class Language(Base):
    __tablename__ = "languages_table"

    name = Column(String, primary_key=True)
    countries = relationship("CountryLanguage", back_populates="language")


class CountryLanguage(Base):
    __tablename__ = "country_language"

    country_name = Column(String, ForeignKey('countries_table.name'),
                          primary_key=True)
    language_name = Column(String, ForeignKey('languages_table.name'),
                           primary_key=True)
    order = Column(Integer)
    language = relationship("Language", back_populates="countries")
    country = relationship("Country", back_populates="languages")


class Currency(Base):
    __tablename__ = "currencies"

    code = Column(String, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    countries = relationship("CountryCurrency", back_populates="currency")


class CountryCurrency(Base):
    __tablename__ = "country_currency"

    country_name = Column(String, ForeignKey('countries_table.name'),
                          primary_key=True)
    currency_code = Column(String, ForeignKey('currencies.code'),
                           primary_key=True)
    order = Column(Integer)
    currency = relationship("Currency", back_populates="countries")
    country = relationship("Country", back_populates="currencies")


# Create the tables in the database
Base.metadata.create_all(engine)


def get_engine():
    return engine
