import streamlit as st
import foodFunction

def run():
    st.set_page_config(
        page_title="Data Mining Individual Assignment 1 ",
        page_icon="👋",
    )

    st.write("Japanese Food Recommendation System")
    # Using the function from the imported module
    result = foodFunction.recommendFood()
    
    st.write("Result:", result)


if __name__ == "__main__":
    run()
