import streamlit as st
import demo

def run():
    st.set_page_config(
        page_title="Data Mining Individual Assignment 1 ",
        page_icon="👋",
    )

    st.write("Japanese Food Recommendation System")
    # Define a list of values for the dropdown
    options = ["California Roll", "Salmon Nigiri", "Tonkotsu Ramen", "Chicken Teriyaki Bento", "Edamame", "Gyoza (Dumplings)", "Tempura (Shrimp)", 
            "Green Tea Ice Cream", "Mochi Ice Cream", "Matcha Latte"]
    
    # Create the dropdown list using selectbox
    selected_option = st.selectbox('Select an option:', options)
    
    # Display the selected option
    st.write('You selected:', selected_option)


if __name__ == "__main__":
    run()
