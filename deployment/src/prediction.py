import joblib
import streamlit as st
import pandas as pd
import base64
from pathlib import Path
import joblib
import imblearn

MODEL_PATH = Path(__file__).resolve().parent / "best_model.joblib"
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)
best_model = load_model()

CURRENT_DIR = Path(__file__).resolve().parent
SIU_PATH = CURRENT_DIR / "ronaldo_siu.gif"
SAD_PATH = CURRENT_DIR / "sad-ronaldo.gif"



def run():
    # Open and read local gif file
    with SIU_PATH.open("rb") as file:
        siu = base64.b64encode(file.read()).decode("utf-8")
    with SAD_PATH.open("rb") as file:
        sad = base64.b64encode(file.read()).decode("utf-8")
        
    with st.form("shooting"):
      
      competition = st.text_input("Competition Name: ", value = "    ")
      season = st.text_input("Season: ", value = "    ")
      team = st.text_input("Team Name: ", value = "    ")
      player = st.text_input("Player Name: ", value = "    ")
      under_pressure = st.selectbox("Under Pressure:", (True, False))
      shot_body_part_name = st.selectbox("Shot Body Part:", ('Head', 'Right Foot', 'Left Foot', 'Other'))
      shot_technique_name = st.selectbox("Shot Technique:", ('Normal', 'Half Volley', 'Volley', 'Lob', 
                                                             'Diving Header', 'Overhead Kick', 'Backheel'))
      shot_type_name = st.selectbox("Shot Type:", ('Open Play', 'Free Kick', 'Penalty', 'Corner', 'Kick Off'))
      play_pattern_name = st.selectbox("Shot Type:", ('From Corner', 'Regular Play', 'From Free Kick', 
                                                      'From Throw In','From Kick Off', 'From Goal Kick', 
                                                      'From Counter', 'From Keeper', 'Other'))
      distance_to_goal = st.slider("Distance to Goal: ", min_value = 0, max_value = 130, value = 20)
      angle_to_goal = st.slider("Angle to Goal: ", min_value = 0, max_value = 90, value = 0)
      submitted = st.form_submit_button("Predict")


    data_inf = {
            "competition_name": competition
            ,"season_name": season
            ,"team": team
            ,"player": player
            ,"under_pressure": under_pressure
            ,"shot_body_part_name":	shot_body_part_name
            ,"shot_technique_name":	shot_technique_name
            ,"shot_type_name":	shot_type_name
            ,"play_pattern_name": play_pattern_name	
            ,"distance_to_goal": distance_to_goal	
            ,"angle_to_goal": angle_to_goal
            }

    data_inf = pd.DataFrame([data_inf])

    if submitted:
        st.write("## Shot Profile:", data_inf)

        pred = best_model.predict(data_inf)

        pred_proba = best_model.predict_proba(data_inf)

        #display
        st.write("## Goal Probability :", pred_proba)
        st.write("## Is goal? :", int(pred[0]))

        if int(pred[0]) == 1:
          st.markdown(
                  f'<img src="data:image/gif;base64,{siu}" alt="gif">',
                  unsafe_allow_html=True,)
        else:
          st.markdown(
                  f'<img src="data:image/gif;base64,{sad}" alt="gif">',
                  unsafe_allow_html=True,)

if __name__ == "__main__":
    run()
