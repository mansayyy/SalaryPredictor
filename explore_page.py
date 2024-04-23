import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'Less than 1 year':
        return 0.5
    elif x== 'More than 50 years':
        return 55
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

def clean_age(x):
    if 'Under 18 years old' in x:
        return 16
    if '18-24 years old' in x:
        return 21
    if '25-34 years old' in x:
        return 30
    if '45-54 years old' in x:
        return 50
    if '35-44 years old' in x:
        return 40
    if '55-64 years old' in x:
        return 60
    if '65 years or older' in x:
        return 70
    return 35

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment" ,"Age", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly" : "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)
    #Remove small countries and put them in Other category
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df.Country.value_counts()

    #Salary
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']

    df['YearsCodePro']= df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df['Age'] = df['Age'].apply(clean_age)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Developer Salaries")
    st.write("""### Stack Overflow Developer Survey 2023""")
    

    data_country = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True).reset_index()
    chart_country = alt.Chart(data_country).mark_bar(color='#8ECAE6').encode(
        x=alt.X('Country', sort='-y'),
        y='Salary'
    ).properties(
    width='container'  # Set width to match container width
    )
    st.write("""#### Mean Salary by Country""")
    st.altair_chart(chart_country, use_container_width=True) 

    data_experience = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True).reset_index()
    chart_experience = alt.Chart(data_experience).mark_line(color='#219EBC').encode(
        x='YearsCodePro',
        y='Salary'
    ).properties(
        width='container'  # Set width to match container width
    )
    st.write("""#### Mean Salary by Experience""")
    st.altair_chart(chart_experience, use_container_width=True)  # Set use_container_width=True

    data = df["Country"].value_counts()

    #Make Pie Chart using MatplotLib
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    st.write(""" #### Number of Data from different countries""")
    st.pyplot(fig1)
    