import json
import random
from textblob import TextBlob
from pdf2image import convert_from_path  # for PDF to image conversion
from PIL import Image  # for image processing
import pytesseract  # for OCR (text extraction from images)
from datetime import datetime  # for timestamp


def generate_random_id():
    return str(random.randint(1, 1000))


def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"


def load_topic_keywords():
    with open("JSON/topic_keywords.json", 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def process_text(content, topic_keywords):
    # Process the text and perform sentiment analysis
    overall_sentiment = get_sentiment(content)

    # Initialize topics dictionary
    topics_data = {}

    # Process each topic
    for topic, keywords in topic_keywords.items():
        topic_data = {"keywords": keywords, "paragraphs": []}

        # Process paragraphs for the current topic
        for paragraph in content.split('\n'):
            if any(keyword in paragraph.lower() for keyword in keywords):
                sentiment = get_sentiment(paragraph)
                topic_data["paragraphs"].append({"content": paragraph, "sentiment": sentiment})

        # Add topic data to topics dictionary only if there are paragraphs for the topic
        if topic_data["paragraphs"]:
            topics_data[topic] = topic_data

    # For simplicity, we'll assume one label and one topic ("general") for text input
    labels = ["general"]

    return {
        "id": generate_random_id(),
        "content": content,
        "labels": labels,
        "sentiment": overall_sentiment,
        "topics": topics_data
    }


def process_image(image_path, topic_keywords):
    # Convert image to text using OCR
    text_content = pytesseract.image_to_string(Image.open(image_path))

    # Process the text extracted from the image
    return process_text(text_content, topic_keywords)


def process_pdf(pdf_path, topic_keywords):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    text_content = ""

    # Extract text from each image
    for image in images:
        text_content += pytesseract.image_to_string(image)

    # Process the text extracted from the PDF
    return process_text(text_content, topic_keywords)


def main():
    topic_keywords = load_topic_keywords()

    user_input = input("Enter the path to a text file, screenshot, or PDF: ")

    if user_input.lower().endswith(('.txt', '.pdf', '.png', '.jpg', '.jpeg')):
        if user_input.lower().endswith('.txt'):
            with open(user_input, 'r', encoding='utf-8') as file:
                content = file.read()
                article_data = process_text(content, topic_keywords)
        elif user_input.lower().endswith(('.png', '.jpg', '.jpeg')):
            article_data = process_image(user_input, topic_keywords)
        elif user_input.lower().endswith('.pdf'):
            article_data = process_pdf(user_input, topic_keywords)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_json_path = f"output_article_{timestamp}.json"
        with open(output_json_path, 'w', encoding='utf-8') as output_json_file:
            json.dump(article_data, output_json_file, ensure_ascii=False, indent=2)
        print(f"Article data has been saved to {output_json_path}")
    else:
        print("Unsupported file format. Please provide a text file, screenshot, or PDF.")


if __name__ == "__main__":
    main()
