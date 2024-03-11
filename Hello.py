import streamlit as st
import pandas as pd
import numpy as np
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


if __name__ == "__main__":
    run()
