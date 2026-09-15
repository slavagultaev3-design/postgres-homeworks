"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import os
import psycopg2

DB_CONFIG = {
    "dbname": "north",
    "user": "postgres",
    "password": "1111",  # Сюда впишите ваш пароль от PostgreSQL
    "host": "localhost",
    "port": "5432"
}

def load_csv(cursor, file_name, insert_query):
    file_path = os.path.join("north_data", file_name)
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл {file_path} не найден!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cursor.execute(insert_query, row)

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("Подключение к базе данных прошло успешно!")
    except Exception as e:
        print(f"Не удалось подключиться к базе данных:\n{e}")
        return

    try:
        print("Загрузка клиентов...")
        insert_cust = "INSERT INTO customers VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;"
        load_csv(cursor, "customers_data.csv", insert_cust)

        print("Загрузка сотрудников...")
        insert_emp = "INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;"
        load_csv(cursor, "employees_data.csv", insert_emp)

        print("Загрузка заказов...")
        insert_ord = "INSERT INTO orders VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;"
        load_csv(cursor, "orders_data.csv", insert_ord)

        conn.commit()
        print("Все данные успешно перенесены в БД!")

    except Exception as e:
        conn.rollback()
        print(f"Произошла ошибка при импорте данных: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

