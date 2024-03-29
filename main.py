from database.db_manager import DBManager
from database.hh_vacansies import HH_api_db
from config import config
from database.utils import create_database, create_table


def main():
    params_db = config()
    create_database('hh_db', params_db)
    create_table(params_db)
    db_vacancies = HH_api_db()
    db_vacancies.employers_to_db()
    db_vacancies.vacancies_to_db()


if __name__ == '__main__':
    main()

    print(DBManager.get_vacancies_with_keyword('python'))
    print(DBManager.get_vacancies_with_higher_salary())
    print(DBManager.get_all_vacancies())
    print(DBManager.get_avg_salary())
    print(DBManager.get_companies_and_vacancies_count())

