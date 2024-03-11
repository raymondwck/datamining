import streamlit as st
from streamlit.logger import get_logger
import Assignment 1 (1)
def run():
    st.set_page_config(
        page_title="Data Mining Individual Assignment 1 ",
        page_icon="👋",
    )

    st.write("Japanese Food Recommendation System")
    # Using the function from the imported module
    result = Assignment 1 (1).recommendFood()
    
    st.write("Result:", result)


if __name__ == "__main__":
    run()
