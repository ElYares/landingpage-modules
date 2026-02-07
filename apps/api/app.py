from flask import Flask, g, Request, Response
from flask_cors import CORS
from strawberry.flask.views import GraphQLView

from landing_api.db import SessionLocal
from landing_api.graphql.schema import schema


class LandingGraphQLView(GraphQLView):
    def get_context(self, request: Request, response: Response):
        # Strawberry por default pone {"request": request}
        # aquí agregamos la sesión DB para usarla en resolvers: info.context["db"]
        return {"request": request, "db": g.db}


app = Flask(__name__)
CORS(app)


@app.before_request
def _open_db_session():
    g.db = SessionLocal()


@app.teardown_request
def _close_db_session(exc):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()


app.add_url_rule(
    "/graphql",
    view_func=LandingGraphQLView.as_view(
        "graphql_view",
        schema=schema,
        graphql_ide="graphiql",
    ),
)


@app.get("/health")
def http_health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

