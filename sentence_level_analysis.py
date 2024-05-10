import json
import random
from datetime import datetime
from transformers import pipeline
from PIL import Image
import pytesseract
from pdf2image import convert_from_path


def generate_random_id():
    return str(random.randint(1, 1000))


def get_sentiment_bert(text):
    sentiment_pipeline = pipeline("sentiment-analysis")
    result = sentiment_pipeline(text)
    return result[0]['label']


def load_keywords_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


from collections import Counter


def process_text(content, topic_keywords, positive_keywords, negative_keywords, biased_terms, aggressive_terms):
    # Initialize topics dictionary
    topics_data = {}

    # Process each topic
    for topic, keywords in topic_keywords.items():
        topic_data = {"keywords": keywords, "sentences": []}

        # Process sentences for the current topic
        sentences = content.split('.')
        sentence_sentiments = []

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                sentiment = get_sentiment_bert(sentence)
                sentence_sentiments.append(sentiment)

                # You can further analyze sentences using your custom keyword lists if needed
                positive_match = any(keyword in sentence.lower() for keyword in positive_keywords)
                negative_match = any(keyword in sentence.lower() for keyword in negative_keywords)
                biased_match = any(keyword in sentence.lower() for keyword in biased_terms)
                aggressive_match = any(keyword in sentence.lower() for keyword in aggressive_terms)

                topic_data["sentences"].append({
                    "content": sentence.strip(),
                    "sentiment": sentiment,
                    "positive_match": positive_match,
                    "negative_match": negative_match,
                    "biased_match": biased_match,
                    "aggressive_match": aggressive_match
                })

        # Determine the majority sentiment for the topic
        if sentence_sentiments:
            majority_sentiment = Counter(sentence_sentiments).most_common(1)[0][0]
            topic_data["majority_sentiment"] = majority_sentiment

            # Add topic data to topics dictionary
            topics_data[topic] = topic_data

    # Determine the overall sentiment based on the majority sentiment across all topics
    all_sentiments = [data["majority_sentiment"] for data in topics_data.values() if "majority_sentiment" in data]
    overall_sentiment = Counter(all_sentiments).most_common(1)[0][0] if all_sentiments else "neutral"

    # For simplicity, we'll assume one label and one topic ("general") for text input
    labels = ["general"]

    return {
        "id": generate_random_id(),
        "content": content,
        "labels": labels,
        "sentiment": overall_sentiment,
        "topics": topics_data
    }


def process_image(image_path, topic_keywords, positive_keywords, negative_keywords, biased_terms, aggressive_terms):
    # Convert image to text using OCR
    text_content = pytesseract.image_to_string(Image.open(image_path))

    # Process the text extracted from the image
    return process_text(text_content, topic_keywords, positive_keywords, negative_keywords, biased_terms,
                        aggressive_terms)


def process_pdf(pdf_path, topic_keywords, positive_keywords, negative_keywords, biased_terms, aggressive_terms):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    text_content = ""

    # Extract text from each image
    for image in images:
        text_content += pytesseract.image_to_string(image)

    # Process the text extracted from the PDF
    return process_text(text_content, topic_keywords, positive_keywords, negative_keywords, biased_terms,
                        aggressive_terms)


def main():
    topic_keywords = load_keywords_from_file("json/topic_keywords.json")
    positive_keywords = load_keywords_from_file("json/positive_keywords.json")
    negative_keywords = load_keywords_from_file("json/negative_keywords.json")
    biased_terms = load_keywords_from_file("json/biased_terms.json")
    aggressive_terms = load_keywords_from_file("json/aggressive_terms.json")

    user_input = input("Enter the path to a text file, screenshot, or PDF: ")

    if user_input.lower().endswith(('.txt', '.pdf', '.png', '.jpg', '.jpeg')):
        if user_input.lower().endswith('.txt'):
            with open(user_input, 'r', encoding='utf-8') as file:
                content = file.read()
                article_data = process_text(content, topic_keywords, positive_keywords, negative_keywords, biased_terms,
                                            aggressive_terms)
        elif user_input.lower().endswith(('.png', '.jpg', '.jpeg')):
            article_data = process_image(user_input, topic_keywords, positive_keywords, negative_keywords, biased_terms,
                                         aggressive_terms)
        elif user_input.lower().endswith('.pdf'):
            article_data = process_pdf(user_input, topic_keywords, positive_keywords, negative_keywords, biased_terms,
                                       aggressive_terms)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_json_path = f"output_article_{timestamp}.json"
        with open(output_json_path, 'w', encoding='utf-8') as output_json_file:
            json.dump(article_data, output_json_file, ensure_ascii=False, indent=2)
        print(f"Article data has been saved to {output_json_path}")
    else:
        print("Unsupported file format. Please provide a text file, screenshot, or PDF.")


if __name__ == "__main__":
    main()
