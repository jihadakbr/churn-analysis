import pandas as pd
import streamlit as st
import plotly.express as px

st.title('Dashboard')

# Adds a line break
st.markdown("<br>", unsafe_allow_html=True)

# Read the CSV file into a DataFrame
train = pd.read_csv('pie_chart.csv')

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



