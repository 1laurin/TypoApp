import json
import re

def identify_terms(content, biased_terms, opinion_terms, positive_keywords, negative_keywords, aggressive_words):
    tokens = re.findall(r'\b\w+\b', content)

    identified_biased_terms = [term.lower() for term in biased_terms if term.lower() in tokens]
    identified_opinion_terms = [term.lower() for term in opinion_terms if term.lower() in tokens]
    identified_positive_keywords = [term.lower() for term in positive_keywords if term.lower() in tokens]
    identified_negative_keywords = [term.lower() for term in negative_keywords if term.lower() in tokens]
    identified_aggressive_words = [word.lower() for word in aggressive_words if word.lower() in tokens]

    return identified_biased_terms, identified_opinion_terms, identified_positive_keywords, identified_negative_keywords, identified_aggressive_words

def save_identified_terms_to_json(identified_terms):
    with open('identified_terms.json', 'w', encoding='utf-8') as output_json_file:
        json.dump(identified_terms, output_json_file, ensure_ascii=False, indent=2)

with open('output_article_20231127161226.json', 'r') as file:
    json_data = json.load(file)

content = json_data.get('content', '')

with open('JSON/biased_terms.json', 'r') as file:
    biased_terms = json.load(file)['biased_terms']

with open('JSON/opinion_based_terms.json', 'r') as file:
    opinion_terms = json.load(file)['opinion_based_terms']

with open('JSON/positive_keywords.json', 'r') as file:
    positive_keywords = json.load(file)['positive_keywords']

with open('JSON/negative_keywords.json', 'r') as file:
    negative_keywords = json.load(file)['negative_keywords']

with open('JSON/aggressive_terms.json', 'r') as file:
    aggressive_words = json.load(file)['aggressive_words']

biased_terms, opinion_terms, positive_terms, negative_terms, aggressive_words = identify_terms(content, biased_terms, opinion_terms, positive_keywords, negative_keywords, aggressive_words)

identified_terms = {
    "biased_terms": biased_terms,
    "opinion_terms": opinion_terms,
    "positive_keywords": positive_terms,
    "negative_keywords": negative_terms,
    "aggressive_words": aggressive_words
}

save_identified_terms_to_json(identified_terms)

print("Identified Biased Terms:", biased_terms)
print("Identified Opinion Terms:", opinion_terms)
print("Identified Positive Keywords:", positive_terms)
print("Identified Negative Keywords:", negative_terms)
print("Identified Aggressive Words:", aggressive_words)
