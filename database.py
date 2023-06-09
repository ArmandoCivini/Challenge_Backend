from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select, text
from sqlalchemy.orm import declarative_base, relationship, Session

# Make the engine
engine = create_engine("sqlite+pysqlite:///:memory:", future=True, echo=False)

# Make the DeclarativeMeta
Base = declarative_base()


class Country(Base):
    __tablename__ = "countries"

    name = Column(String, primary_key=True)
    capital = Column(String)
    currencies = relationship('Currency',
                              secondary='country_currency',
                              back_populates='countries'
                              )
    continent = Column(String)
    languages = relationship('Language',
                             secondary='country_language',
                             back_populates='countries'
                             )
    population = Column(Integer)
    flag = Column(String)
    area = Column(Integer)


class Currency(Base):
    __tablename__ = "currencies"

    code = Column(String, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    countries = relationship('Country',
                             secondary='country_currency',
                             back_populates='currencies'
                             )


class CountryCurrency(Base):
    __tablename__ = "country_currency"

    country_name = Column(String, ForeignKey('countries.name'),
                          primary_key=True)
    currency_code = Column(String, ForeignKey('currencies.code'),
                           primary_key=True)


class Language(Base):
    __tablename__ = "languages"

    name = Column(String, primary_key=True)
    countries = relationship('Country',
                             secondary='country_language',
                             back_populates='languages'
                             )


class CountryLanguage(Base):
    __tablename__ = "country_language"

    country_name = Column(String, ForeignKey('countries.name'),
                          primary_key=True)
    language_name = Column(String, ForeignKey('languages.name'),
                           primary_key=True)

# Create the tables in the database
Base.metadata.create_all(engine)

# Test it
with Session(bind=engine) as session:

    # add users
    usr1 = Country(name="bob")
    session.add(usr1)

    usr2 = Country(name="alice")
    session.add(usr2)

    session.commit()

    # add projects
    prj1 = Language(name="Project 1")
    session.add(prj1)

    prj2 = Language(name="Project 2")
    session.add(prj2)

    session.commit()

    # map users to projects
    prj1.countries = [usr1]
    prj1.countries.append(usr2)
    prj2.countries = [usr2]

    session.commit()


with Session(bind=engine) as session:

    print(session.query(Country).where(Country.name == "bob").one().languages[0].name)
    print(session.query(Language).where(Language.name == "Project 2").one().countries)
    stmt = select('*').select_from(text("country_language"))
    print(session.execute(stmt).fetchall())
