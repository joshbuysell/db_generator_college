import importlib
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import load_schema, create_mysql_database_if_not_exists
from flasgger import Swagger, swag_from
import sqlalchemy

schema = load_schema()
db_uri = schema["database"]["uri"]

db_name = sqlalchemy.engine.url.make_url(db_uri).database

if db_uri.startswith("mysql"):
    create_mysql_database_if_not_exists(db_uri, db_name)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
swagger = Swagger(app)
models = {}

for table in schema["tables"]:
    columns = {}
    for col in table["columns"]:
        col_type = getattr(importlib.import_module("sqlalchemy"), col["type"])
        args = []
        if col["type"] == "String" and "length" in col:
            args = [col["length"]]
        params = {}
        if col.get("primary_key"):
            params["primary_key"] = True
        if col.get("autoincrement"):
            params["autoincrement"] = True
        columns[col["name"]] = db.Column(col_type(*args), **params)
    model = type(table["name"].capitalize(), (db.Model,), columns)
    models[table["name"]] = model

with app.app_context():
    db.create_all()
    for table in schema["tables"]:
        model = models[table["name"]]
        if db.session.query(model).count() == 0 and "data" in table:
            for row in table["data"]:
                obj = model(**row)
                db.session.add(obj)
    db.session.commit()

for table in schema["tables"]:
    route = f"/api/{table['name']}"
    model = models[table["name"]]

    def make_list(model, table):
        @swag_from({
            'responses': {200: {"description": f"List of {table['name']}", "examples": {"application/json": []}}},
            'tags': [table['name']],
            'parameters': [],
        })
        def list_items():
            items = model.query.all()
            result = [{c.name: getattr(x, c.name) for c in x.__table__.columns} for x in items]
            return jsonify(result)
        return list_items

    def make_create(model, table):
        @swag_from({
            'responses': {200: {"description": f"Created {table['name']}", "examples": {"application/json": {}}}},
            'tags': [table['name']],
            'parameters': [{
                "in": "body",
                "name": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {col['name']: {"type": "string"} for col in table["columns"] if col["name"] != "id"}
                }
            }],
        })
        def create_item():
            obj = model(**request.json)
            db.session.add(obj)
            db.session.commit()
            d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
            return jsonify(d)
        return create_item

    def make_read(model, table):
        @swag_from({
            'responses': {200: {"description": f"Read {table['name']} by id", "examples": {"application/json": {}}}},
            'tags': [table['name']],
            'parameters': [{
                "name": "id",
                "in": "path",
                "type": "integer",
                "required": True,
            }],
        })
        def read_item(id):
            obj = model.query.get_or_404(id)
            d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
            return jsonify(d)
        return read_item

    def make_update(model, table):
        @swag_from({
            'responses': {200: {"description": f"Update {table['name']} by id", "examples": {"application/json": {}}}},
            'tags': [table['name']],
            'parameters': [
                {
                    "name": "id",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                },
                {
                    "in": "body",
                    "name": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {col['name']: {"type": "string"} for col in table["columns"] if col["name"] != "id"}
                    }
                }
            ],
        })
        def update_item(id):
            obj = model.query.get_or_404(id)
            for k, v in request.json.items():
                setattr(obj, k, v)
            db.session.commit()
            d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
            return jsonify(d)
        return update_item

    def make_delete(model, table):
        @swag_from({
            'responses': {200: {"description": f"Delete {table['name']} by id", "examples": {"application/json": {"message": "Deleted"}}}},
            'tags': [table['name']],
            'parameters': [{
                "name": "id",
                "in": "path",
                "type": "integer",
                "required": True,
            }],
        })
        def delete_item(id):
            obj = model.query.get_or_404(id)
            db.session.delete(obj)
            db.session.commit()
            return jsonify({"message": "Deleted"})
        return delete_item

    app.add_url_rule(route, f"{table['name']}_list", make_list(model, table), methods=["GET"])
    app.add_url_rule(route, f"{table['name']}_create", make_create(model, table), methods=["POST"])
    app.add_url_rule(f"{route}/<int:id>", f"{table['name']}_read", make_read(model, table), methods=["GET"])
    app.add_url_rule(f"{route}/<int:id>", f"{table['name']}_update", make_update(model, table), methods=["PUT"])
    app.add_url_rule(f"{route}/<int:id>", f"{table['name']}_delete", make_delete(model, table), methods=["DELETE"])

if __name__ == "__main__":
    app.run(debug=True)