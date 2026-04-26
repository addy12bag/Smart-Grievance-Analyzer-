from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model + vectorizer
try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except Exception as e:
    print("❌ Error loading model:", e)
    exit()

# ✅ Health check route
@app.route("/")
def home():
    return "Smart Grievance API is running 🚀"

# Priority logic
def get_priority(text):
    text = text.lower()

    high_keywords = ["accident", "fire", "danger", "urgent"]
    medium_keywords = ["not working", "issue", "problem"]

    if any(word in text for word in high_keywords):
        return "High"
    elif any(word in text for word in medium_keywords):
        return "Medium"
    else:
        return "Low"

# Department mapping
def get_department(category):
    mapping = {
        "Road": "Public Works Department",
        "Water": "Water Supply Department",
        "Electricity": "Electricity Board",
        "Sanitation": "Municipal Corporation",
        "Noise": "Police Department"
    }
    return mapping.get(category, "General Department")

# ✅ Main prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Validate JSON
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        text = str(data["text"]).strip()

        if not text:
            return jsonify({"error": "Empty text provided"}), 400

        # Transform + predict
        vec = vectorizer.transform([text])
        category = model.predict(vec)[0]

        # Extra logic
        priority = get_priority(text)
        department = get_department(category)

        return jsonify({
            "category": category,
            "priority": priority,
            "department": department
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run server
if __name__ == "__main__":
    app.run(debug=True)