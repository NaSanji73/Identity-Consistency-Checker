from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Simple skill list
SKILLS = ["python", "java", "c", "javascript", "machine learning", "data science", "html", "css", "git"]

# Extract skills from text
def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return found

# Get GitHub languages
def get_github_data(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    data = response.json()

    languages = []
    for repo in data:
        if repo.get("language"):
            languages.append(repo["language"].lower())

    return list(set(languages)), len(data)

# Calculate score
def calculate_score(skills, languages, repo_count):
    verified = []
    weak = []
    unverified = []

    score = 0

    for skill in skills:
        if skill in languages:
            verified.append(skill)
            score += 15
        else:
            weak.append(skill)
            score += 5

    # bonus for activity
    if repo_count > 5:
        score += 10

    score = min(score, 100)

    return score, verified, weak, unverified

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data["text"]
    github = data["github"]

    skills = extract_skills(text)
    languages, repo_count = get_github_data(github)

    score, verified, weak, unverified = calculate_score(skills, languages, repo_count)

    return jsonify({
        "skills": skills,
        "verified": verified,
        "weak": weak,
        "score": score,
        "repos": repo_count
    })

if __name__ == "__main__":
    app.run(debug=True)