import streamlit as st

def printRule(premise, conclusion, support, confidence, features):
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    st.write("Rule: If a person buys {0} they will also buy {1}".format(premise_name, conclusion_name))
    st.write("- Confidence: {0:.3f}".format(confidence[(premise, conclusion)]))
    st.write("- Support: {0}".format(support[(premise, conclusion)]))
    st.write("")
    
def run():
    st.set_page_config(
        page_title="Data Mining Individual Assignment 1 ",
        page_icon="👋",
    )

    st.write("Japanese Food Recommendation System")
    # Define a list of values for the dropdown
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
   
    # Create the dropdown list using selectbox
    selected_option = st.selectbox('Select an option:', options)
    
    # Display the selected option
    st.write('You selected:', selected_option)

    features = ["California Roll", "Salmon Nigiri", "Tonkotsu Ramen", "Chicken Teriyaki Bento", "Edamame", "Gyoza (Dumplings)", "Tempura (Shrimp)", 
            "Green Tea Ice Cream", "Mochi Ice Cream", "Matcha Latte"]

    from collections import defaultdict
    df = pd.read_excel("JapanMenuItems.xlsx")

    X = df.values
    n_samples, n_features = X.shape

    # Now compute for all possible rules
    valid_rules = defaultdict(int)
    invalid_rules = defaultdict(int)
    num_occurences = defaultdict(int)
    
    for sample in X:
        for premise in range(n_features):
            if sample[premise] == 0: continue
            # Record that the premise was bought in another transaction
            num_occurences[premise] += 1
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
        confidence[(premise, conclusion)] = valid_rules[(premise, conclusion)] / num_occurences[premise]
        
    sorted_confidence = sorted(confidence.items(), key=itemgetter(1), reverse=True)
    
    # Find the index of the user-input premise in the features list
    premise_index = features.index(selected_option)

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

    # Print the top three rules
    for i, rule in enumerate(sorted_rules[:3]):
        print("Rule #{0}".format(i + 1))
        printRule(rule[0], rule[1], support, confidence, features)

    if st.button("Recommend"):
        # Call the recommendFood function passing the user input
        recommended_food = recommendFood(selected_option)

        # Display recommended food or rules
        if recommended_food:
            st.write("Recommended food:", recommended_food)
        else:
            st.write("No recommendation found.")



if __name__ == "__main__":
    run()
