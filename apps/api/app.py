from flask import Flask
from flask_cors import CORS
import strawberry
from strawberry.flask.views import GraphQLView

@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"
    
schema = strawberry.Schema(query=Query)

app = Flask(__name__)
CORS(app)

app.add_url_rule(

    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True)
)

@app.get("/health")
def http_health():
    return {"status":"ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
