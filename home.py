import streamlit as st

st.title('Churn Analysis: Predicting Customer Attrition')

# Adds a line break
st.markdown("<br>", unsafe_allow_html=True)

st.info("Welcome to the Customer Churn Prediction App!")


st.info("""
    Customer churn is one of the biggest challenges faced by financial institutions today. 
    
    In this app, I use machine learning to predict customer churn, helping you understand which factors are driving customers to leave.

    My model analyzes customer data, including demographics, transaction behaviors, and interaction history to predict whether a customer is likely to churn.
""")

st.info("""
    With insights derived from feature importance analysis, you'll get a clear understanding of which attributes matter most in churn prediction.

    Whether you're in customer service, marketing, or data science, this tool can help you make more informed decisions to retain your most valuable customers.
""")

st.info("Explore the app and see how my model can make a difference!")
