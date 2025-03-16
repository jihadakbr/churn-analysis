import streamlit as st

# Set page config to wide layout
st.set_page_config(layout='wide')

# Apply custom CSS for hover effect and styling
st.markdown("""
    <style>
        /* Increase radio button size */
        div[data-testid="stRadio"] label {
            font-size: 18px !important;
            padding: 10px 8px;
        }

        /* Improve spacing */
        div[data-testid="stSidebar"] {
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation with styled radio buttons
st.sidebar.title('🚀 Churn App')
st.sidebar.markdown('Made using Streamlit by **Jihad Akbar**')

page = st.sidebar.radio(
    "## 📌 Navigate", 
    [
        "🏠 Home",
        "📊 Dashboard",
        "🛠️ Apps",
        "📞 Contact"
    ],
)

# Display content based on the selected page
pages = {
    "🏠 Home": "home.py",
    "📊 Dashboard": "dashboard.py",
    "🛠️ Apps": "apps.py",
    "📞 Contact": "contact.py",
}

with open(pages[page]) as f:
    exec(f.read())
