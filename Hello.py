import streamlit as st
from operator import itemgetter
from collections import defaultdict

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
        return "If a person buys {0}, they will also buy {1}. Confidence: {2:.3f}, Support: {3}".format(
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

# Load the Excel file into a DataFrame
df = pd.read_excel('JapanMenuItems.xlsx')
X = df.values
n_features = 3  # Number of food items
features = ["California Roll", "Salmon Nigiri", "Tonkotsu Ramen", "Chicken Teriyaki Bento", "Edamame", "Gyoza (Dumplings)", "Tempura (Shrimp)", 
            "Green Tea Ice Cream", "Mochi Ice Cream", "Matcha Latte"]
def main():
    st.title("Food Recommendation System")

    # User input for initial food order
    initial_order = st.text_input("Enter your initial food order (e.g., burger, pizza, sushi):")

    if st.button("Get Recommendations"):
        # Call recommendFood function
        recommendations = recommendFood(initial_order, X, n_features, features)

        # Display recommendations
        st.subheader("Top 3 Recommendations based on your initial order:")
        for i, rule in enumerate(recommendations):
            st.write(f"Recommendation #{i+1}: {printRule(*rule, support, confidence, features)}")

if __name__ == "__main__":
    main()
