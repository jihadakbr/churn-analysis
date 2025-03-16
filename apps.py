import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load your pre-trained model
model = joblib.load('churn_recall_91.xgb')

# Preprocessing function
def preprocess_input():
    # Create a row with two columns
    tab1, tab2 = st.columns(2)

    with tab1:
        gender = st.selectbox("Gender", options=["Male", "Female"])
        gender_encoded = 1 if gender == "Male" else 0  # Female -> 0, Male -> 1
        
        dependent_count = st.number_input("Number of Dependents", min_value=0, max_value=10, value=0)
        education_level = st.selectbox("Education Level", options=["College", "Doctorate", "Graduate", "High School", "Post-Graduate", "Uneducated", "Unknown"])
        marital_status = st.selectbox("Marital Status", options=["Divorced", "Married", "Single", "Unknown"])
        income_category = st.selectbox("Income Category", options=["$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K", "Unknown"])
        card_category = st.selectbox("Card Category", options=["Blue", "Gold", "Platinum", "Silver"])
        months_on_book = st.number_input("Months as a Customer", min_value=1, max_value=100, value=12)    
        total_relationship_count = st.number_input("Number of Products Used", min_value=1, max_value=20, value=5)

    with tab2:
        months_inactive_12_mon = st.number_input("Months Inactive in Last 12 Months", min_value=0, max_value=12, value=0)
        contacts_count_12_mon = st.number_input("Number of Interactions in Last 12 Months", min_value=0, max_value=30, value=0)
        credit_limit = st.number_input("Credit Limit ($)", min_value=1000.0, max_value=50000.0, value=5000.0, step=0.1, format="%0.1f")
        total_revolving_bal = st.number_input("Total Amount of Funds Used ($)", min_value=0.0, max_value=5000.0, value=100.0, step=0.1, format="%0.1f")
        total_amt_chng_q4_q1 = st.number_input("Increase in Transaction Amount (Q4 to Q1)", min_value=0.0, max_value=10.0, value=0.0, step=0.001, format="%0.3f")
        total_trans_ct = st.number_input("Total Number of Transactions in the Last 12 Months", min_value=0, max_value=200, value=10)
        total_ct_chng_q4_q1 = st.number_input("Increase in the Number of Transactions (Q4 to Q1)", min_value=0.0, max_value=10.0, value=0.0, step=0.001, format="%0.3f")
        avg_utilization_ratio = st.number_input("Percentage of Credit Card Usage", min_value=0.0, max_value=1.0, value=0.1, step=0.001, format="%0.3f")

    # Create a DataFrame for numerical features
    df = pd.DataFrame({
        'gender': [gender_encoded],
        'dependent_count': [dependent_count],
        'months_on_book': [months_on_book],
        'total_relationship_count': [total_relationship_count],
        'months_inactive_12_mon': [months_inactive_12_mon],
        'contacts_count_12_mon': [contacts_count_12_mon],
        'credit_limit': [credit_limit],
        'total_revolving_bal': [total_revolving_bal],
        'total_amt_chng_q4_q1': [total_amt_chng_q4_q1],
        'total_trans_ct': [total_trans_ct],
        'total_ct_chng_q4_q1': [total_ct_chng_q4_q1],
        'avg_utilization_ratio': [avg_utilization_ratio]
    })

    # One-hot encode marital_status
    marital_status_columns = ['marital_status_Divorced', 'marital_status_Married', 'marital_status_Single', 'marital_status_Unknown']
    for col in marital_status_columns:
        df[col] = [1 if marital_status in col else 0]

    # One-hot encode card_category
    card_category_columns = ['card_category_Blue', 'card_category_Gold', 'card_category_Platinum', 'card_category_Silver']
    for col in card_category_columns:
        df[col] = [1 if card_category in col else 0]

    # One-hot encode education_level
    education_columns = ['education_level_College', 'education_level_Doctorate', 'education_level_Graduate', 
                         'education_level_High School', 'education_level_Post-Graduate', 
                         'education_level_Uneducated', 'education_level_Unknown']
    for col in education_columns:
        df[col] = [1 if education_level in col else 0]

    # One-hot encode income_category
    income_columns = ['income_category_$120K +', 'income_category_$40K - $60K', 'income_category_$60K - $80K', 
                      'income_category_$80K - $120K', 'income_category_Less than $40K', 'income_category_Unknown']
    for col in income_columns:
        df[col] = [1 if income_category in col else 0]

    # Drop unnecessary columns
    drop_columns = ['marital_status_Divorced', 'card_category_Blue', 'education_level_College', 'income_category_$120K +']
    df.drop(columns=drop_columns, inplace=True)

    return df

# Title of the Streamlit app
st.title("Customer Churn Prediction")

# Adds a line break
st.markdown("<br>", unsafe_allow_html=True) 

st.write(
    "Welcome to the Customer Churn Prediction tool. This application allows you to input customer data, "
    "and it will predict whether the customer is likely to churn (attrited) or remain a customer."
    " Please fill out the following form with the customer's details."
)

# Create the data for the table
data = {
    'Model': ['XGBoost'],
    'Recall': ['91%'],
    'Precision': ['70%'],
    'F1-Score': ['79%'],
    'Threshold': ['0.45']
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Display in Streamlit
st.dataframe(df, hide_index=True)


# Collect the user input
processed_input = preprocess_input()

# Function to predict based on input with a custom threshold
def make_prediction(input_data, threshold=0.45):
    # Reshape the input data to be 2D as expected by the model
    input_array = np.array(input_data).reshape(1, -1)  # Reshaping to 2D array

    # Get predicted probabilities (probabilities for class 1)
    y_pred_proba = model.predict_proba(input_array)[:, 1]
    
    # Apply the custom threshold to classify based on probability
    prediction = 1 if y_pred_proba >= threshold else 0
    return prediction, y_pred_proba

# Button to make a prediction
if st.button("Predict Churn"):
    # Show a loading spinner while processing
    with st.spinner("Predicting... please wait."):
        # Get the prediction and probability
        prediction, probability = make_prediction(processed_input, threshold=0.45)
        
    # Display the result
    st.subheader("Prediction Result")
    st.write(f"The model predicts: **{'Attrited Customer (Class 1)' if prediction == 1 else 'Existing Customer (Class 0)'}**")
    st.write(f"Predicted Probability (Threshold = 0.45): **{probability[0]:.4f}**")

    # Add feedback for the user
    if prediction == 1:
        st.error("This customer is likely to churn.")
    else:
        st.success("This customer is likely to stay.")

st.write("---")

st.header('Sample of the Customer')

# Adds a line break
st.markdown("<br>", unsafe_allow_html=True)

# Define the data for the table
data = {
    'Features': ['Gender', 'Number of Dependents', 'Education Level', 'Marital Status', 'Income Category', 
                 'Card Category', 'Month as a Customer', 'Number of Products Used', 'Months Inactive in Last 12 Months', 
                 'Number of Interactions in Last 12 Months', 'Credit Limit ($)', 'Total Amount of Funds Used ($)', 
                 'Increase in Transaction Amount (Q4 to Q1)', 'Total Number of Transactions in the Last 12 Months', 
                 'Increase in the Number of Transactions (Q4 to Q1)', 'Percentage of Credit Card Usage'],
    'Existing Customer 1': ['Male', 1, 'Graduate', 'Married	', '$80K - $120K', 'Blue', 36, 5, 3, 2, 6313.0, 782, 0.931, 34, 0.889, 0.124],
    'Existing Customer 2': ['Female', 4, 'Unknown', 'Married', 'Less than $40K', 'Blue', 46, 5, 3, 2, 4271.0, 1150, 1.064, 50, 0.724, 0.269],
    'Attrited Customer 1': ['Male', 3, 'Graduate', 'Married', '$60K - $80K', 'Blue', 28, 2, 3, 2, 6407.0, 478, 1.022, 77, 0.833, 0.075],
    'Attrited Customer 2': ['Female', 2, 'High School', 'Single', 'Less than $40K', 'Blue', 46, 6, 1, 2, 3199.0, 0, 1.047, 59, 0.639, 0.000]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Add a custom index starting from 1 and set it to the 'Features' column
df.index = [i + 1 for i in range(len(df))]

# Display the DataFrame with a fixed height to prevent vertical scrolling
st.dataframe(df, height=600)