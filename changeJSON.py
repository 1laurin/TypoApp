import json

# Load the existing sentiment_dict
with open('sentiment_dict.json', 'r') as f:
    old_sentiment_dict = json.load(f)

# Create a new dictionary for the modified format
new_sentiment_dict = {}

# Iterate through each topic in the old sentiment_dict
for topic, topic_values in old_sentiment_dict.items():
    new_sentiment_dict[topic] = {}

    # Iterate through each typology in the topic_values
    for typology, sentiment in topic_values.items():
        if sentiment not in new_sentiment_dict[topic]:
            new_sentiment_dict[topic][sentiment] = [typology]
        else:
            new_sentiment_dict[topic][sentiment].append(typology)

# Save the new sentiment_dict to a file
with open('new_sentiment_dict1.json', 'w') as f:
    json.dump(new_sentiment_dict, f, indent=4)

print("Conversion complete. New sentiment_dict saved to 'new_sentiment_dict.json'")
