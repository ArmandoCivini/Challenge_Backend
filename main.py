from sqlalchemy import (create_engine, Column, Integer,
                        String, Table, ForeignKey)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from data_fetcher import get_countries_data
from sqlalchemy import select


engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# data = get_countries_data()
# for country in data:
#     if "languages" not in country.keys():
#         continue
#     if len(country["languages"]) > 1:
#         print(country["languages"])

# association_table = Table(
#     "contry_currencies",
#     Base.metadata,
#     Column("country", ForeignKey("countries.name")),
#     Column("currency", ForeignKey("currencies.code")),
# )


class Country(Base):
    __tablename__ = "countries"

    name = Column(String, primary_key=True)
    capital = Column(String)
    currencies = relationship('Currency', secondary="contry_currencies", back_populates="countries")
    continent = Column(String)
    language = Column(String)
    population = Column(Integer)
    flag = Column(String)


class Currency(Base):
    __tablename__ = "currencies"

    code = Column(String, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    contries = relationship('Country', secondary="contry_currencies", back_populates="currencies")


class ProjectUser(Base):
    __tablename__ = "contry_currencies"

    country_name = Column(Integer, ForeignKey("countries.name"), primary_key=True)
    currency_code = Column(Integer, ForeignKey("currencies.code"), primary_key=True)


Base.metadata.create_all(engine)


country = Country(name="Jordan", capital="algo", population=3)
session.add(country)
# curr = Currency(code="JOD", name="Jordanian Dinar", symbol="JD")
# session.add(curr)
# country.currencies.append(curr)
# print(session.query(Country).filter_by(name="Jordan").first())
# print(session.query(Country).filter_by(name="Jordan").first().currencies[0].code)
# stmt = select('*').select_from(association_table)
# print(session.execute(stmt).fetchall())
