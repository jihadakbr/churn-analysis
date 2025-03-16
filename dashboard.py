# import joblib
# import dalex as dx
import pandas as pd
import streamlit as st
import plotly.express as px

# Load your pre-trained model
# model = joblib.load('churn_recall_91.xgb')

st.title('Dashboard')

# Adds a line break
st.markdown("<br>", unsafe_allow_html=True)

# Read the CSV file into a DataFrame
train = pd.read_csv('pie_chart.csv')
# train_fi = pd.read_csv('feature_importance_train.csv')

st.header('Attrited Rate Distribution (Total: 8101)')
pie_1, pie_2= st.columns(2)
with pie_1:
    # Count the occurrences of each category in the 'attrition_flag' column
    attrition_counts = train['attrition_flag'].value_counts()

    # Create a plotly pie chart
    fig = px.pie(values=attrition_counts, names=attrition_counts.index)

    # Update the font size for title and labels, and position the legend
    fig.update_layout(
        font=dict(size=18),  # Increase the font size for labels
        legend=dict(
            font=dict(size=16),  # Increase the font size for legend
            x=0,  # Move legend to the left
            y=1,  # Move legend to the top
            xanchor="left",  # Anchor legend to the left
            yanchor="top"  # Anchor legend to the top
        )
    )

    # Display the pie chart in Streamlit
    st.plotly_chart(fig)


with pie_2:
    # Adds a line break
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.info("""
    The target distribution is imbalanced, with 83.9% (6799) existing customers and 16.1% (1302) attrited customers (5:1).
    """)

    st.info("""
    This means for every 5 existing customers, only 1 customer has churned. It's important to address this imbalance as it could impact our strategies for customer retention and acquisition.
    """)

# Calculate churn rate by age group
train['age_group'] = pd.cut(train['customer_age'], bins=range(20, 80, 3))

# Convert the age group intervals into strings
train['age_group'] = train['age_group'].astype(str)

churn_by_age = train.groupby('age_group')['attrition_flag'].apply(lambda x: (x == 'Attrited Customer').mean()).reset_index()

# Streamlit header
st.header('Churn Rate by Age Group')

# Add a toggle button for sorting
sort_order = st.checkbox('Sort from highest to lowest churn rate')

# Sort the data if checkbox is checked
if sort_order:
    churn_by_age = churn_by_age.sort_values(by='attrition_flag', ascending=False)

# Create Plotly bar chart
fig = px.bar(churn_by_age, 
             x='age_group', 
             y='attrition_flag', 
             labels={'age_group': 'Age Group (years)', 'attrition_flag': 'Churn Rate (%)'}
             )

# Change the bar color to red
fig.update_traces(marker_color='red')

# Update the font size for x-tick, y-tick, x-label, and y-label
fig.update_layout(
    xaxis=dict(
        tickfont=dict(size=14),  # Increase font size for x-ticks
        title_font=dict(size=16)  # Increase font size for x-label
    ),
    yaxis=dict(
        tickfont=dict(size=14),  # Increase font size for y-ticks
        title_font=dict(size=16)  # Increase font size for y-label
    ),
)

# Display the plot in Streamlit
st.plotly_chart(fig)

st.info("""
        Based on the Churn Rate by Age Group plot, the age groups with the highest churn rates are 29-32 years and 53-59 years. 
        """)
st.info("""
        These two age groups exhibit the largest proportion of churned customers relative to the total number of customers within those groups.
        """)
st.info("""
         The 29-32 and 53-59 age groups show a notable spike in churn rates, suggesting that customers in these age ranges are more likely to churn compared to other age groups.         
         """)

# Adds a line break
st.markdown("<br>", unsafe_allow_html=True)

st.header('Feature Distribution')

# Show the columns in the dataset to understand which are categorical and numerical
# Select categorical columns (object data type)
categorical_columns = train.select_dtypes(include=['object']).columns
categorical_columns = [col for col in categorical_columns if col != 'attrition_flag'] # exclude attrition_flag
numerical_columns = train.select_dtypes(include=['number']).columns

histogram_1, histogram_2= st.columns(2)
with histogram_1:
    # Select box for categorical column for pie chart
    selected_categorical = st.selectbox('Select a categorical column for Pie Chart', categorical_columns)

    # Calculate value counts for the selected categorical column
    value_counts = train[selected_categorical].value_counts().reset_index()
    value_counts.columns = [selected_categorical, 'count']

    # Merge the value counts back into the main dataframe to use for hovertemplate
    train_with_counts = train.merge(value_counts, how='left', on=selected_categorical)

    # Create Pie Chart
    fig_pie = px.pie(
        train_with_counts,
        names=selected_categorical,
        title=f'Pie Chart for {selected_categorical}',
        hole=0.3,  # Optional: makes the pie chart into a donut chart
    )

    # Add hover information to show both percentage and the count
    fig_pie.update_traces(
        textinfo='percent+label',
        hovertemplate=(
            '%{label}: %{value} (%{percent:.2f}%)<br>'
            'Count: %{customdata[0]}'
        ),
        customdata=train_with_counts[selected_categorical].map(
            value_counts.set_index(selected_categorical)['count']
        )
    )

    # Update Layout for bigger size and larger fonts
    fig_pie.update_layout(
        title_font_size=24,  # Title font size
        legend_title_font_size=18,  # Legend title font size
        legend_font_size=16,  # Legend font size
        font=dict(size=16),  # General font size
        width=800,  # Width of the chart
        height=600,  # Height of the chart
    )

    # Display Pie Chart
    st.plotly_chart(fig_pie)

with histogram_2:
    # Select box for numerical column for histogram
    selected_numerical = st.selectbox('Select a numerical column for Histogram', numerical_columns)

    # Create Histogram
    fig_hist = px.histogram(train, x=selected_numerical, title=f'Histogram for {selected_numerical}')

    # Update Layout
    fig_hist.update_layout(
        xaxis_title='',  # Remove x-axis title
        yaxis_title='',  # Remove y-axis title
        xaxis=dict(
            showticklabels=True,  # Keep x-tick labels
            tickfont=dict(size=16)  # Increase size of x-ticks
        ),
        yaxis=dict(
            showticklabels=True,  # Keep y-tick labels
            tickfont=dict(size=16)  # Increase size of y-ticks
        ),
        title_font_size=24,  # Title font size
        width=800,  # Width of the chart
        height=600,  # Height of the chart
    )

    # Display Histogram
    st.plotly_chart(fig_hist)


####### Feature Importance #######

# Prepare the data
# X_train = train_fi.drop(['attrition_flag'], axis=1)
# y_train = train_fi['attrition_flag']

# # Save the Explainer object
# explainer = dx.Explainer(model, X_train, y_train, label='XGBoost', verbose=False)

# # Generate the feature importance plot
# fig = explainer.model_parts().plot()

# # Ensure the figure is passed to Streamlit in a way that aligns with the new requirements
# # Create a Matplotlib figure and axes explicitly if needed
# fig, ax = plt.subplots()
# explainer.model_parts().plot(ax=ax)

# # Display the plot in Streamlit
# st.pyplot(fig)

st.header('Feature Importance')

st.image('img/feature-importance.png')

st.info("Key Predictors of Churn: **total_trans_ct** (Total number of transactions)")
st.info("This feature is the most important predictor in the model, suggesting that customers with a higher number of transactions are less likely to churn.")
st.info("Customers with a total transaction count (total_trans_ct) of less than or equal to 20 are more likely to churn, as indicated by the predicted probability of > 0.499 (with our threshold set at 0.4501). ")
st.info("Since total_trans_ct is the strongest predictor, improving transaction frequency could help reduce churn.")