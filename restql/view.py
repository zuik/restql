import json

import sqlalchemy
from flask import Flask, request, g, jsonify, abort
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from utils import AlchemyEncoder

app = Flask(__name__)
app.json_encoder = AlchemyEncoder


def create_session():
    if "DB_URI" not in app.config:
        raise Exception("What is the database we are connecting to?")

    uri = app.config.get("DB_URI")
    engine = create_engine(uri, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_session():
    if "session" not in g:
        g.session = create_session()
        return g.session
    else:
        return g.session


def create_endpoint(model1, model2=None):
    table = model1.__table__  # type: sqlalchemy.schema.Table
    table_name = table.name

    if model2 is not None:
        join_table = model2.__table__
        join_table_name = join_table.name

    @app.route(f"/{table_name}")
    def select_all():
        session = get_session()
        finalize = request.args.get("finalize", "all")
        if finalize == "all":
            r = session.query(model1).all()
            return jsonify(r)
        else:
            return abort(400)

    @app.route(f"/{table_name}/filter")
    def filter():
        session = get_session()
        q = session.query(model1)

        filter = json.loads(request.args.get("filter"))
        print(filter)
        if filter:
            for k, v in filter.items():
                if k == "&&":
                    # Then v is the things that we need to and
                    q = handle_logic_op(k, q, v[0])
                    q = handle_logic_op(k, q, v[1])
                else:
                    q = handle_logic_op(k, q, v)

        finalize = request.args.get("finalize", "all")
        if finalize != "all":
            return abort(400)
        else:
            return jsonify(q.all())

    def handle_logic_op(key, q, v):
        if "eq" in v.keys():
            q = q.filter(getattr(model1, key) == v["eq"])
        elif "lt" in v.keys():
            # Handle <
            q = q.filter(getattr(model1, key) < v["lt"])
        elif "lte" in v.keys():
            # Handle <=
            q = q.filter(getattr(model1, key) <= v["lte"])
        elif "gt" in v.keys():
            # Handle >
            q = q.filter(getattr(model1, key) > v["gt"])
        elif "gte" in v.keys():
            # Handle >=
            q = q.filter(getattr(model1, key) >= v["gte"])
        return q

    @app.route(f"/{table_name}/orderBy")
    def orderBy():
        session = get_session()
        q = session.query(model1)

        orderBy = json.loads(request.args.get("orderBy"))
        print(orderBy)
        if orderBy:
            for k, v in orderBy.items():
                if (v["asc"]):
                    q = q.order_by(getattr(model1, k))
                else:
                    q = q.order_by(getattr(model1, k).desc())
        finalize = request.args.get("finalize", "all")
        if finalize != "all":
            return abort(400)
        else:
            return jsonify(q.all())

    @app.route(f"/{table_name}/join")
    def join():
        session = get_session()

        if request.args.get("join") == None:
            q = session.query(model1, model2)
            finalize = request.args.get("finalize", "all")
            if finalize != "all":
                return abort(400)
            else:
                return jsonify(q.all())
        else:
            q = session.query(model1, model2)
            join = json.loads(request.args.get("join"))
            print(join)
            if join:
                for k, v in join.items():
                    if "filter" in v.keys():
                        q = q.filter(getattr(model1, k) == getattr(model2, v["filter"]))

        finalize = request.args.get("finalize", "all")
        if finalize != "all":
            return abort(400)
        else:
            return jsonify(q.all())

    return app


@app.teardown_appcontext
def shutdown_session(exception=None):
    ''' Enable Flask to automatically remove database sessions at the
     end of the request or when the application shuts down.
     Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
    '''
    if hasattr(g, 'session'):
        g.session.close()


if __name__ == '__main__':
    from model import User, Address

    app.config["DB_URI"] = "sqlite:///test.db"

    app = create_endpoint(User, Address)

    app.run(debug=True)
