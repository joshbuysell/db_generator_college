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
streamlit run streamlit_schema_gen.py
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
streamlit run streamlit_app.py
```

- CRUD-доступ до всіх таблиць (візуальний інтерфейс): http://localhost:8501

---

## Структура проєкту

```
├── app.py                   # Flask REST API, Swagger, ORM
├── config.py                # Робота з schema.json, автоматичне створення БД
├── schema.json              # Опис БД, таблиць, даних (автоматично/вручну)
├── streamlit_app.py         # CRUD веб-інтерфейс (Streamlit)
├── streamlit_schema_gen.py  # Генератор schema.json (Streamlit)
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

---

## FAQ

- **Потрібно більше таблиць/записів?**  
  Просто опиши в schema.json.
- **Не працює підключення до БД?**  
  Перевір URI і права користувача.
- **Хочеш PostgreSQL чи SQLite?**  
  Зміни URI на потрібний формат.

---


