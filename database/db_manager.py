import psycopg2
from database.hh_vacansies import params_db


class DBManager:

    @staticmethod
    def get_companies_and_vacancies_count():
        with psycopg2.connect(dbname='hh_db', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, COUNT(vacancy_name) from vacancies GROUP BY company_name')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_all_vacancies():
        with psycopg2.connect(dbname='hh_db', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * from vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_avg_salary():
        with psycopg2.connect(dbname='hh_db', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT avg(salary) from vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_vacancies_with_higher_salary():
        with psycopg2.connect(dbname='hh_db', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name from vacancies WHERE salary > (SELECT AVG(salary) from vacancies)')
                answer = cur.fetchall()
        conn.close()
        return answer

    @staticmethod
    def get_vacancies_with_keyword(keyword):
        with psycopg2.connect(dbname='hh_db', **params_db) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT vacancy_name from vacancies WHERE vacancy_name LIKE '%{keyword}%'")
                answer = cur.fetchall()
        conn.close()
        return answer
