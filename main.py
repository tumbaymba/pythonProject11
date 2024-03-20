from database.hh_vacansies import HH_api_db
from config import config
from database.utils import create_database, create_table
from database.db_manager import DBManager


def main():
    params_db = config()
    create_database(database_name='hh_db', **params_db)
    create_table(**params_db)
    db_vacancies = HH_api_db()
    db_vacancies.employers_to_db()
    db_vacancies.vacancies_to_db()


if __name__ == '__main__':
    main()
