import eda
import prediction
import streamlit as st

page =  st.sidebar.selectbox("Select Page", ("EDA", "Prediction"))

if page == "EDA":
    eda.run()

elif page == "Prediction":
    prediction.run()