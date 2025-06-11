from flask import Flask, request, jsonify
import os
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from your frontend domain

# Set your OpenAI API key as environment variable OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/review", methods=["POST"])
def review_resume():
    data = request.json
    resume_text = data.get("resume", "")

    if not resume_text:
        return jsonify({"feedback": "Please provide your resume text."}), 400

    try:
        prompt = (
            "You are an expert career coach. "
            "Please review the following resume and give concise, constructive feedback:\n\n"
            f"{resume_text}\n\nFeedback:"
        )

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
        )
        feedback = response.choices[0].text.strip()
        return jsonify({"feedback": feedback})

    except Exception as e:
        return jsonify({"feedback": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
