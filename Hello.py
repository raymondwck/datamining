import streamlit as st
from operator import itemgetter
from collections import defaultdict
import demo
def recommendFood(user_input, X, n_features, features):
    # Now compute for all possible rules
    valid_rules = defaultdict(int)
    invalid_rules = defaultdict(int)
    num_occurrences = defaultdict(int)

    for sample in X:
        for premise in range(n_features):
            if sample[premise] == 0:
                continue
            # Record that the premise was bought in another transaction
            num_occurrences[premise] += 1
            for conclusion in range(n_features):
                if premise == conclusion:  # It makes little sense to measure if X -> X.
                    continue
                if sample[conclusion] == 1:
                    # This person also bought the conclusion item
                    valid_rules[(premise, conclusion)] += 1
                else:
                    # This person bought the premise, but not the conclusion
                    invalid_rules[(premise, conclusion)] += 1
    support = valid_rules
    confidence = defaultdict(float)
    for premise, conclusion in valid_rules.keys():
        confidence[(premise, conclusion)] = valid_rules[(premise, conclusion)] / num_occurrences[premise]

    sorted_support = sorted(support.items(), key=itemgetter(1), reverse=True)
    sorted_confidence = sorted(confidence.items(), key=itemgetter(1), reverse=True)

    def printRule(premise, conclusion, support, confidence, features):
        premise_name = features[premise]
        conclusion_name = features[conclusion]
        return "Rule: If a person buys {0} they will also buy {1}\n- Confidence: {2:.3f}\n- Support: {3}\n".format(
            premise_name, conclusion_name, confidence[(premise, conclusion)], support[(premise, conclusion)])

    # Find the index of the user-input premise in the features list
    premise_index = features.index(user_input)

    # Create a list to store the rules
    rules = []

    # Iterate over the sorted confidence list
    for index in range(len(sorted_confidence)):
        if len(rules) >= 3:
            break

        (premise, conclusion) = sorted_confidence[index][0]
        premise_name = features[premise]
        conclusion_name = features[conclusion]

        # Check if the premise and conclusion names are different and if the premise matches user input
        if premise_name != conclusion_name and premise == premise_index:
            rules.append((premise, conclusion))

    # Sort the rules based on confidence score
    sorted_rules = sorted(rules, key=lambda x: confidence[x], reverse=True)

    return sorted_rules[:3]

import pandas as pd
import requests
from io import BytesIO

# URL of the Excel file
url = 'https://github.com/raymondwck/datamining/raw/77e7ff11d72d28afeaa2f850cc03c5bfe6893fc8/JapanMenuItems.xlsx'

# Download the Excel file from the URL
response = requests.get(url)
if response.status_code == 200:
    # Read the Excel file from the response content
    df = pd.read_excel(BytesIO(response.content))
    # Display the DataFrame
    print(df)
else:
    print("Failed to download the Excel file.")

X = df.values
n_features = 3  # Number of food items
features = ["California Roll", "Salmon Nigiri", "Tonkotsu Ramen", "Chicken Teriyaki Bento", "Edamame", "Gyoza (Dumplings)", "Tempura (Shrimp)", 
            "Green Tea Ice Cream", "Mochi Ice Cream", "Matcha Latte"]

def main():
    st.title("Food Recommendation System")
    # Define your options for the dropdown
    options = {
        "California Roll": 0,
        "Salmon Nigiri": 1,
        "Tonkotsu Ramen": 2,
        "Chicken Teriyaki Bento": 3,
        "Edamame": 4,
        "Gyoza (Dumplings)": 5,
        "Tempura (Shrimp)": 6,
        "Green Tea Ice Cream": 7,
        "Mochi Ice Cream": 8,
        "Matcha Latte": 9
    }
    
        # User input for initial food order using dropdown
    initial_order = st.selectbox("Select your initial food order:", options)

    if st.button("Get Recommendations"):
        # Call recommendFood function
        recommendations = recommendFood(initial_order, X, n_features, features)

        # Display recommendations
        st.subheader("Top 3 Recommendations based on your initial order:")
        st.write(recommendations)

if __name__ == "__main__":
    main()
