from database_schema import Country


def get_all_countries(session):
    return session.query(Country).all()
