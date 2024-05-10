import json
from datetime import datetime

# Assuming load_identified_terms and load_output_data functions are needed
def load_identified_terms():
    # Implement this function to load data from identified_terms.json
    # Example: replace 'identified_terms.json' with the actual file path or API endpoint
    with open('output/identified_terms.json', 'r') as file:
        identified_terms_data = json.load(file)
    return identified_terms_data

def load_output_data():
    # Implement this function to load data from output{timestamp}.json
    # Example: replace 'output{timestamp}.json' with the actual file path or API endpoint
    with open('OUTPUT/output_article_20231127114949.json', 'r') as file:
        output_data = json.load(file)
    return output_data

def load_sentiment_dict():
    # Load sentiment dictionary from the sentiment_dict.json file
    with open('JSON/typology_sentiment_analysis.json', 'r') as file:
        sentiment_dict = json.load(file)
    return sentiment_dict

def adjust_sentiment_based_on_typology(sentiment, typology_sentiments, sentiment_dict, topic):
    adjusted_scores = {}

    # Find the topic in the sentiment_dict
    topic_data = next((item for item in sentiment_dict.get('topics', []) if item.get('name') == topic), {})

    if topic_data:
        typology_attributes = topic_data.get('attributes', [])

        for typology in typology_sentiments:
            # Find the sentiment in the typology_attributes
            typology_sentiment = next((attr.get('sentiment', 0) for attr in typology_attributes if attr.get('Typology') == typology), 0)

            # Set the original sentiment based on the values in sentiment_dict
            original_sentiment = get_sentiment_score(typology_sentiment)
            print(f"Original sentiment for {typology}: {original_sentiment}")

            sentiment_adjustment = typology_sentiments.get(typology, 0)

            adjusted_scores[typology] = original_sentiment + sentiment_adjustment

    return adjusted_scores


def get_sentiment_score(sentiment):
    sentiment_mapping = {"positive": 1, "negative": -1, "neutral": 0}

    if isinstance(sentiment, str):
        return sentiment_mapping.get(sentiment.lower(), 0)
    elif isinstance(sentiment, int):
        return sentiment
    elif isinstance(sentiment, dict):  # Handle cases where sentiment is a dictionary
        return sentiment_mapping.get(sentiment.get("sentiment", "").lower(), 0)
    else:
        # Handle other cases if needed
        return 0


if __name__ == "__main__":
    identified_terms_data = load_identified_terms()
    output_data = load_output_data()
    sentiment_dict = load_sentiment_dict()  # Load the sentiment dictionary

    for topic, topic_data in output_data["topics"].items():
        for paragraph in topic_data["paragraphs"]:
            # Adjust this line based on your actual data structure
            sentiment = get_sentiment_score(paragraph.get("sentiment", "neutral"))
            typology_sentiments = paragraph.get("typology_sentiment", {})
            print(f"Typology sentiments for paragraph: {typology_sentiments}")

            adjusted_scores = adjust_sentiment_based_on_typology(sentiment, typology_sentiments, sentiment_dict, topic)
            paragraph["adjusted_scores"] = adjusted_scores

            print(f"Adjusted scores: {adjusted_scores}")

    # Save the output with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"OUTPUT/sentiment_results_{timestamp}.json"

    with open(output_filename, "w") as output_file:
        json.dump(output_data, output_file, indent=2)

    print(f"Sentiment results saved to: {output_filename}")
