# CRUD Generator: Flask + Streamlit +  schema.json

## Опис

Цей проєкт — автоматизований CRUD генератор на Python:
- Створює БД (MySQL, SQLite) і таблиці за схемою
- Піднімає REST API з CRUD для кожної сутності (Flask, SQLAlchemy)
- Swagger-документація генерується автоматично
- Дані та схема задаються у schema.json (генерується через Streamlit-форму) якщо потрібно
- Веб-інтерфейс на Streamlit для перегляду, редагування, додавання, видалення даних
- Генератор schema.json на Streamlit

---

## Швидкий старт

### 1. Встановлення

pip install -r requirements.txt

### 2. Генерація schema.json

- Запусти генератор схеми:
```bash
streamlit run ui_generator_schema.py
```
- Заповни форму: URI БД, таблиці, поля, стартові дані
- Скачай schema.json і поклади у корінь проєкту

### 3. Генерація/оновлення БД та запуск API

```bash
python app.py or flask run
```

- Створиться база, таблиці, заповняться стартові дані, згенерується CRUD для всіх сутностей
- Swagger UI: http://localhost:5000/apidocs

### 4. Веб-інтерфейс для роботи з таблицями (CRUD GUI)

```bash
streamlit run ui_table.py
```

- CRUD-доступ до всіх таблиць (візуальний інтерфейс): http://localhost:8501

---

## Структура проєкту

```
├── app.py                   # Flask REST API, Swagger, ORM
├── config.py                # Робота з schema.json, автоматичне створення БД
├── schema.json              # Опис БД, таблиць, даних (автоматично/вручну)
├── ui_table.py         # CRUD веб-інтерфейс (Streamlit)
├── ui_generator_schema.py  # Генератор schema.json (Streamlit)
├── requirements.txt         # Залежності
└── README.md                # Інструкція
```

---

## Як це працює

1. **Описуєш БД у schema.json** (вручну або через Streamlit-генератор)
2. **Запускаєш app.py** — створюється база, таблиці, заповнюються дані, піднімається CRUD API з документацією
3. **Можеш працювати через REST API, Swagger, або Streamlit CRUD GUI**

---

## Заміна структури або даних

- Змінив schema.json — просто перезапусти `app.py` і все оновиться!
## Приклад schema.json

Ця схема описує базу даних із п’ятьма таблицями:

- **users**
  Зберігає користувачів.
  - `id`: Integer, PK, autoincrement
  - `name`: String(50)
  - `email`: String(100)
  Містить 8 користувачів (Alice, Bob, Carol, ...).

- **posts**
  Пости користувачів.
  - `id`: Integer, PK, autoincrement
  - `user_id`: Integer (автор)
  - `title`: String(100)
  - `body`: Text
  Містить 8 постів, кожен прив’язаний до користувача.

- **comments**
  Коментарі до постів.
  - `id`: Integer, PK, autoincrement
  - `post_id`: Integer
  - `user_id`: Integer (автор коментаря)
  - `content`: String(200)
  8 коментарів до різних постів.

- **categories**
  Категорії для постів.
  - `id`: Integer, PK, autoincrement
  - `name`: String(50)
  7 категорій (News, Personal, Technology, ...).

- **post_categories**
  Зв’язок багато-до-багатьох між постами та категоріями.
  - `id`: Integer, PK, autoincrement
  - `post_id`: Integer
  - `category_id`: Integer
  8 зв’язків між постами та категоріями.

**URI БД:**
`mysql+pymysql://login:password@localhost:3306/demo_db`

Ця структура дозволяє зберігати користувачів, їхні пости, коментарі, категорії та зв’язки між постами й категоріями.
---

## FAQ

- **Потрібно більше таблиць/записів?**
  Просто опиши в schema.json.
- **Не працює підключення до БД?**
  Перевір URI і права користувача.
- **Хочеш PostgreSQL чи SQLite?**
  Зміни URI на потрібний формат.

---



## Examples

# Generator Schema
![Alt text](examples/generator_schema.png?raw=true "Generator Schema")

# CRUD Swagger
![Alt text](examples/swagger.png?raw=true "CRUD Swagger")

# View Table UI
![Alt text](examples/table_ui.png?raw=true "View Table UI")

# Example Diagram
![Alt text](examples/diagram.png?raw=true "Diagram")
