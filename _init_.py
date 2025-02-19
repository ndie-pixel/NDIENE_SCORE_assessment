import azure.functions as func
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/add_score", methods=["POST"])
def add_score():
    data = request.json
    return jsonify(data), 200


def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.WsgiMiddleware(app.wsgi_app).handle(req)