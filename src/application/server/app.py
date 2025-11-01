from flask import Flask, jsonify, request
from flask_cors import CORS
from rag.query_data import query_rag

app = Flask(__name__)
CORS(app)

@app.route("/")
async def async_example():
    return jsonify({"message": "Hello world"})

@app.route("/ask", methods=["POST"])
async def ask():
    data = request.get_json()
    if not data or "question" not in data or "user_id" not in data:
        return jsonify({"error": "Missing 'question' or 'user_id' in request body"}), 400

    question = data["question"]
    user_id = data["user_id"]

    answer = query_rag(question, user_id=user_id)

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
