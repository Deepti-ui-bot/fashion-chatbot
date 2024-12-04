from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Context to store user's details
user_context = {"season": None, "type": None, "gender": None}

# Outfit suggestions
outfit_suggestions = {
    "casual": {
        "summer": {"men": "a casual t-shirt and shorts", "women": "a sundress or a light top with shorts"},
        "winter": {"men": "a cozy sweater with jeans", "women": "a warm cardigan with leggings"},
        "spring": {"men": "a light hoodie with jeans", "women": "a floral dress or a light blouse with jeans"},
        "fall": {"men": "a layered sweater with jeans", "women": "a cozy sweater dress or layered sweater with leggings"},
    },
    "formal": {
        "summer": {"men": "a light blazer with a button-up shirt", "women": "a tailored blazer with a midi dress"},
        "winter": {"men": "a thick woolen suit with a tie", "women": "an elegant long-sleeve dress"},
        "spring": {"men": "a tailored blazer with chinos", "women": "a chic wrap dress or skirt suit"},
        "fall": {"men": "a dark suit with a tie", "women": "a formal blouse with trousers or an elegant dress"},
    },
    "wedding": {
        "summer": {"men": "a light beige or pastel suit with a tie", "women": "a flowy maxi dress or chiffon gown"},
        "winter": {"men": "a deep-colored tuxedo with a bow tie", "women": "a velvet gown with a shawl"},
        "spring": {"men": "a pastel suit with a boutonnière", "women": "a floral print gown or pastel dress"},
        "fall": {"men": "a tailored dark suit with a tie", "women": "a sophisticated gown with autumn tones"},
    },
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_outfit', methods=['POST'])
def get_outfit():
    global user_context
    data = request.json
    query = data.get('query', '').lower()

    # Extract gender, type, and season from the query
    genders = ["men", "women"]
    types = ["casual", "formal", "wedding"]
    seasons = ["summer", "winter", "spring", "fall"]

    detected_gender = None
    detected_type = None
    detected_season = None

    # Check for gender, type, and season in the query
    for gender in genders:
        if gender in query:
            detected_gender = gender
    for outfit_type in types:
        if outfit_type in query:
            detected_type = outfit_type
    for season in seasons:
        if season in query:
            detected_season = season

    # Update context based on detected values (only update the ones that are found)
    if detected_gender:
        user_context["gender"] = detected_gender
    if detected_type:
        user_context["type"] = detected_type
    if detected_season:
        user_context["season"] = detected_season

    # If any context is missing, prompt the user
    if not user_context["type"]:
        return jsonify({"suggestion": "Please specify the outfit type (casual, formal, or wedding)."})
    if not user_context["season"]:
        return jsonify({"suggestion": "Please specify the season (summer, winter, spring, or fall)."})
    if not user_context["gender"]:
        return jsonify({"suggestion": "Please specify the gender (men or women)."})
    
    # Generate suggestion based on the updated context
    selected_type = user_context["type"]
    selected_season = user_context["season"]
    selected_gender = user_context["gender"]

    suggestion = outfit_suggestions[selected_type][selected_season][selected_gender]
    return jsonify({"suggestion": f"For {selected_gender}: {suggestion}."})

if __name__ == '__main__':
    app.run(debug=True)
