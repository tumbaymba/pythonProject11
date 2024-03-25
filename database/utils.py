import psycopg2


def create_database(database_name, params):
    conn = psycopg2.connect(dbname='hh_db', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f'select datname from pg_database  where datname = \'{database_name}\'')
        if cur.fetchall() == 0:
            cur.execute(f'CREATE DATABASE  {database_name}')
    except psycopg2.errors.InvalidCatalogName:
        print('База данных не существует')
    cur.close()
    conn.close()


def create_table(params):
    conn = psycopg2.connect(dbname='hh_db', **params)
    with conn.cursor() as cur:
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (company_id int primary key, company_name varchar unique not null)
                        """)
        except psycopg2.errors.DuplicateTable:
            print('Таблица уже существует 2')

    with conn.cursor() as cur:
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (vacancy_id serial primary key, vacancy_name text not null,
                                        salary int,
                                        company_name text not null,
                                        vacancy_url varchar not null)
                        """)
        except Exception:
            print('Таблица уже существует 3')
    with conn.cursor() as cur:
        try:
            cur.execute("""alter table vacancies add constraint fk_company_name 
            foreign key(company_name) references companies(company_name)""")
        except Exception:
            print('Таблица уже существует')
    conn.commit()
    conn.close()
