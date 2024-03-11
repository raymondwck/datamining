import streamlit as st

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

def recommendFood(selected_option):
    def printRule(premise, conclusion, support, confidence, features):
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    st.write("Rule: If a person buys {0} they will also buy {1}".format(premise_name, conclusion_name))
    st.write("- Confidence: {0:.3f}".format(confidence[(premise, conclusion)]))
    st.write("- Support: {0}".format(support[(premise, conclusion)]))
    st.write("")
    
    # Prompt the user to input a premise
    selected_option = input("Enter a Food Name: ")

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
