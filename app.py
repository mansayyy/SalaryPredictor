import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import pickle
import numpy as np

from predict_page import show_predict_page
from explore_page import show_explore_page

@st.cache
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

def load_config():
    st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
    
def main():
    load_config()
    st.sidebar.title("Explore Or Predict")
    page = st.sidebar.selectbox("", ("Predict", "Explore"))

    if page == "Predict":
        show_predict_page()
    else:
        show_explore_page()

if __name__ == "__main__":
    main()
