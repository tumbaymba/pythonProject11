import psycopg2
import requests
from config import config
params_db = config()


def get_request(employer_id) -> dict:
    params = {
        "page": 1,
        "per_page": 100,
        "employer_id": employer_id,
        "only_with_salary": True,
        "area": 113,
        "only_with_vacancies": True
    }
    return requests.get("https://api.hh.ru/vacancies/", params=params).json()['items']


class HH_api_db:

    employers_dict = {'Роснефть': '6596',
                      'МегаФон': '3127',
                      'МТС': '3776',
                      'Билайн': '4934',
                      'СБЕР': '3529',
                      'Тинькофф': '78638',
                      'Сургуутнефтегаз': '1878711',
                      'Лукойл': '907345',
                      'АО ННК': '6025'}

    def get_vacancies(self):
        vacancies_list = []
        for employer in self.employers_dict:
            emp_vacancies = get_request(self.employers_dict[employer])
            for vacancy in emp_vacancies:
                if vacancy['salary']['from'] is None:
                    salary = 0
                else:
                    salary = vacancy['salary']['from']
                vacancies_list.append(
                    {'url': vacancy['alternate_url'], 'salary': salary,
                     'vacancy_name': vacancy['name'], 'employer': employer})
        return vacancies_list

    def employers_to_db(self):
        with psycopg2.connect(dbname='hh_db', **params_db) as conn:
            with conn.cursor() as cur:
                for employer in self.employers_dict:
                    try:
                        cur.execute(f"INSERT INTO companies values ('{int(self.employers_dict[employer])}', '{employer}')")
                    except Exception:
                        pass
        conn.commit()
        conn.close()

    def vacancies_to_db(self):
        with psycopg2.connect(dbname='hh_db', **params_db) as conn:
            with conn.cursor() as cur:
                for vacancy in self.get_vacancies():
                    cur.execute(
                        f"INSERT INTO vacancies(vacancy_name, salary, company_name, vacancy_url) values "
                        f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
                        f"'{vacancy['employer']}', '{vacancy['url']}')")
        conn.commit()
        conn.close()
