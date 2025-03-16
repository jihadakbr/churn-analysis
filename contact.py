import streamlit as st

# Page title and header
st.title("Contact Information")

# Adds a line break
st.markdown("<br>", unsafe_allow_html=True)  


# Create a row with two columns
contact1, contact2 = st.columns([1,15])

# First column with icons
with contact1:
    st.image("img/person-icon.svg", width=50)
    st.image('img/location-icon.png', width=50)
    st.image('img/phone-icon.svg', width=40)
    st.image('img/gmail-icon.png', width=40)
    st.image('img/linkedin-icon.png', width=45)    
    st.image('img/github-icon.jpg', width=40)

# Second column with text details
with contact2:
    st.subheader('Jihad Akbar')
    st.subheader('Indonesia')
    st.subheader('[(+62) 8133 2326 785](https://wa.me/6281332326785)')
    st.subheader('[jihadakbr@gmail.com](mailto:jihadakbr@gmail.com)')
    st.subheader('[LinkedIn](https://www.linkedin.com/in/jihadakbr)')    
    st.subheader('[Github](https://github.com/jihadakbr)')


# Footer
st.write("---")
st.write("#### Feel free to contact me via the details above!")
