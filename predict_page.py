import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor= data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict the salary""")
    
    countries = ("United States of America",
    'United Kingdom of Great Britain and Northern Ireland','Other',
    'Australia','Netherlands','Germany','Sweden','France','Spain','Brazil',
    'Italy' ,'Canada', 'Switzerland' ,'India', 'Norway' ,'Denmark' ,'Israel',
    'Poland')

    education = ('Bachelor’s degree', 'Less than a Bachelors', 'Master’s degree',
       'Post grad')

    
    country = st.selectbox("Country",countries)
    education = st.selectbox("Education Level",education)
    age = st.slider("Age", 0, 80, 22)
    experience = st.slider("Year of Experience", 0, 50, 3)
    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, experience, age ]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)
        salary = regressor.predict(X)
        st.subheader(f"The estimated salary for software engineer with above specifications is:$ {salary[0]:.2f}")

