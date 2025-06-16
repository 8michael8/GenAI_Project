from flask import Flask, request, jsonify
from models import engine
import openai
import os
from sqlalchemy import text

app = Flask(__name__)
openai.api_key = os.getenv("OPEN_API_KEY")

@app.route('/api/query', methods=['POST'])
def query():
    try:
        question = request.get_json().get("question", "").strip()
        if not question:
            return jsonify({"error": "No question provided"}), 400

        question_embed = openai.embeddings.create(model = "text-embedding-3-small", input = question)
        q_vec = question_embed.data[0].embedding

        sql = text("""
        SELECT t.content AS content, t.citation AS citation, t.title AS title, t.id AS section
        FROM content_embedding e
        JOIN title t ON t.id = e.law_id
        ORDER BY e.embedding <-> CAST(:q_vec AS vector)
        LIMIT 3
        """)

        with engine.connect() as conn:
            outputs = conn.execute(sql, {"q_vec": q_vec}).fetchall()
            print(outputs)

        return jsonify({
            "results": [
                {"content": r.content, "citation": r.citation, "title": r.title, "section": r.section} for r in outputs
            ]
        }), 200

    except Exception as e:
        print(f"Error retrieving question: {e}")
        return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)