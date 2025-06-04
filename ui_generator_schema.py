import streamlit as st
import json

st.title("Генератор schema.json для CRUD генератора")

db_uri = st.text_input("Database URI (наприклад: mysql+pymysql://user:pass@host:port/dbname)", value="sqlite:///test.db")

if "tables" not in st.session_state:
    st.session_state.tables = []

st.subheader("Таблиці")

with st.form("add_table_form", clear_on_submit=True):
    table_name = st.text_input("Назва таблиці")
    submitted = st.form_submit_button("Додати таблицю")
    if submitted and table_name:
        st.session_state.tables.append({
            "name": table_name,
            "columns": [],
            "data": []
        })

for i, table in enumerate(st.session_state.tables):
    expander = st.expander(f"Таблиця: {table['name']}", expanded=False)

    with expander:
        st.write("Поля:")
        for j, col in enumerate(table["columns"]):
            st.write(f"- {col['name']} ({col['type']})"
                     + (f" [{col['length']}]" if "length" in col else "")
                     + (" PK" if col.get("primary_key") else "")
                     + (" AUTOINC" if col.get("autoincrement") else "")
            )

        with st.form(f"add_column_form_{i}", clear_on_submit=True):
            col_name = st.text_input("Назва поля", key=f"col_name_{i}")
            col_type = st.selectbox("Тип", ["Integer", "String", "Text"], key=f"col_type_{i}")
            col_length = st.number_input("Довжина (для String)", min_value=1, value=50, key=f"col_length_{i}")
            col_pk = st.checkbox("Primary key", key=f"col_pk_{i}")
            col_ai = st.checkbox("Autoincrement", key=f"col_ai_{i}")
            add_col = st.form_submit_button("Додати поле")
            if add_col and col_name:
                col = {"name": col_name, "type": col_type}
                if col_type == "String":
                    col["length"] = int(col_length)
                if col_pk:
                    col["primary_key"] = True
                if col_ai:
                    col["autoincrement"] = True
                table["columns"].append(col)

    with expander:
        st.write("Стартові дані (optional):")
        if table["columns"]:
            default_data = {}
            for col in table["columns"]:
                if col.get("primary_key") and col.get("autoincrement"):
                    continue
                default_data[col['name']] = st.text_input(f"{col['name']} для нового запису", key=f"data_{i}_{col['name']}")
            if st.button(f"Додати запис у {table['name']}", key=f"add_data_{i}"):
                data_to_add = {k: v for k, v in default_data.items() if v != ""}
                table["data"].append(data_to_add)
        for rec in table["data"]:
            st.json(rec)

    with expander:
        if st.button(f"Видалити таблицю {table['name']}", key=f"del_table_{i}"):
            st.session_state.tables.pop(i)
            st.experimental_rerun()

schema = {
    "database": {"uri": db_uri},
    "tables": st.session_state.tables
}

st.subheader("Згенерований schema.json")
st.code(json.dumps(schema, indent=2), language="json")

st.download_button(
    label="Скачати schema.json",
    data=json.dumps(schema, indent=2),
    file_name="schema.json",
    mime="application/json"
)