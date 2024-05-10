import json
import re

def identify_terms(content, charged_keywords, biased_terms, opinion_terms, positive_keywords, negative_keywords, aggressive_words):
    # Tokenize the content
    tokens = re.findall(r'\b\w+\b', content)

    # Identify charged keywords
    identified_charged_keywords = [term.lower() for term in charged_keywords if term.lower() in tokens]

    # Identify biased terms
    identified_biased_terms = [term.lower() for term in biased_terms if term.lower() in tokens]

    # Identify opinion terms
    identified_opinion_terms = [term.lower() for term in opinion_terms if term.lower() in tokens]

    # Identify positive keywords
    identified_positive_keywords = [term.lower() for term in positive_keywords if term.lower() in tokens]

    # Identify negative keywords
    identified_negative_keywords = [term.lower() for term in negative_keywords if term.lower() in tokens]

    # Identify aggressive words
    identified_aggressive_words = [word.lower() for word in aggressive_words if word.lower() in tokens]

    return identified_charged_keywords, identified_biased_terms, identified_opinion_terms, identified_positive_keywords, identified_negative_keywords, identified_aggressive_words

# Load the JSON content from file
with open('output_article_20231127163256.json', 'r') as file:
    json_data = json.load(file)

# Extract content from JSON data
content = json_data.get('content', '')

# Load charged keywords, bias terms, opinion terms, positive keywords, negative keywords, and aggressive words from separate JSON files
with open('json/charged_keywords.json', 'r') as file:
    charged_keywords = json.load(file)['politically_charged_words']

with open('JSON/biased_terms.json', 'r') as file:
    biased_terms = json.load(file)['biased_terms']

with open('JSON/opinion_based_terms.json', 'r') as file:
    opinion_terms = json.load(file)['opinion_based_terms']

with open('json/positive_keywords.json', 'r') as file:
    positive_keywords = json.load(file)['positive_keywords']

with open('json/negative_keywords.json', 'r') as file:
    negative_keywords = json.load(file)['negative_keywords']

with open('JSON/aggressive_terms.json', 'r') as file:
    aggressive_words = json.load(file)['aggressive_words']

# Identify terms in the content
charged_keywords, biased_terms, opinion_terms, positive_terms, negative_terms, aggressive_words = identify_terms(content, charged_keywords, biased_terms, opinion_terms, positive_keywords, negative_keywords, aggressive_words)

# Print the identified terms
print("Identified Charged Keywords:", charged_keywords)
print("Identified Biased Terms:", biased_terms)
print("Identified Opinion Terms:", opinion_terms)
print("Identified Positive Keywords:", positive_terms)
print("Identified Negative Keywords:", negative_terms)
print("Identified Aggressive Words:", aggressive_words)
