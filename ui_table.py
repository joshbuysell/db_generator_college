import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from config import load_schema

schema = load_schema()
db_uri = schema["database"]["uri"]
engine = create_engine(db_uri)
metadata = MetaData()
metadata.reflect(bind=engine)

st.title("База даних: CRUD")

table_names = list(metadata.tables.keys())
table = st.selectbox("Оберіть таблицю:", table_names)

if table:
    tbl = Table(table, metadata, autoload_with=engine)
    df = pd.read_sql_table(table, engine)
    st.subheader("Дані")
    st.dataframe(df)

    st.subheader("Додати новий запис")
    add_data = {}
    for col in tbl.columns:
        if col.primary_key and col.autoincrement:
            continue
        add_data[col.name] = st.text_input(f"{col.name}", key=f"add_{col.name}")

    if st.button("Додати"):
        with engine.connect() as conn:
            ins = tbl.insert().values({k: v if v != "" else None for k, v in add_data.items()})
            conn.execute(ins)
            st.success("Додано!")
            st.experimental_rerun()

    st.subheader("Редагувати/Видалити")
    if not df.empty:
        idx = st.selectbox("Виберіть запис", df.index)
        row = df.loc[idx]
        edit_data = {}
        for col in tbl.columns:
            if col.primary_key:
                edit_data[col.name] = row[col.name]
            else:
                edit_data[col.name] = st.text_input(f"edit_{col.name}", value=row[col.name], key=f"edit_{col.name}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Оновити", key=f"upd_{idx}"):
                with engine.connect() as conn:
                    upd = tbl.update().where(tbl.primary_key.columns.values()[0] == row[tbl.primary_key.columns.values()[0].name]).values(
                        {k: v for k, v in edit_data.items() if not tbl.columns[k].primary_key}
                    )
                    conn.execute(upd)
                    st.success("Оновлено!")
                    st.experimental_rerun()
        with col2:
            if st.button("Видалити", key=f"del_{idx}"):
                with engine.connect() as conn:
                    delete = tbl.delete().where(tbl.primary_key.columns.values()[0] == row[tbl.primary_key.columns.values()[0].name])
                    conn.execute(delete)
                    st.warning("Видалено!")
                    st.experimental_rerun()