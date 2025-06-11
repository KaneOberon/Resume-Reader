from flask import Flask, request, jsonify
import os
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://kaneoberon.github.io"])

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/review", methods=["POST"])
def review_resume():
    data = request.json
    resume_text = data.get("resume", "")

    if not resume_text:
        return jsonify({"review": "Please provide your resume text."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert career coach."},
                {"role": "user", "content": f"Please review the following resume and give concise, constructive feedback:\n\n{resume_text}"}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        feedback = response.choices[0].message.content.strip()
        return jsonify({"review": feedback})

    except Exception as e:
        return jsonify({"review": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
