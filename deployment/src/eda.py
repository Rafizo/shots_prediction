import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image
import base64

def run():
    # Open and read local gif file
    file_ = open('ronaldo_score.gif', "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.title("Shooting Prediction")
    # Display local GIF via markdown
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="gif">',
        unsafe_allow_html=True,)

    df = pd.read_csv("P1M2_Muhammad_Rafi_Addien.csv")
    st.dataframe(df)

    shot_rank = df.groupby("player").count().sort_values(by='is_goal',
                                 ascending=False).head()[["is_goal"]]
    shot_rank = shot_rank.rename(columns={"is_goal":"shots"})

    goals = df[df["is_goal"] == 1]



    option1 = st.selectbox(
        "Select Top 5",
        ("Top 5 Most Shots", "Top 5 Most Goals"))

    if option1 == "Top 5 Most Shots":
        st.dataframe(shot_rank)
    if option1 == "Top 5 Most Goals":
        st.dataframe(goals.groupby("player").count().sort_values(by='is_goal', 
            ascending=False).head()[["is_goal"]].rename(columns={"is_goal":"goals"}))
    


    def display():
        fig.update_layout(width=700,height=500,margin=dict(l=20, r=20, t=60, b=20))
        fig.update_traces(automargin=True, textinfo='percent+label')
        st.plotly_chart(fig, width='stretch', theme="streamlit")


    option = st.selectbox(
    "Select Pie Chart",
    ("Goal Shots", "Shots Outcome", "Goal"))

    if option == "Goal Shots":
        df_counts = pd.DataFrame(goals["shot_type_name"].value_counts())
        df_counts.reset_index(inplace=True)
        fig = px.pie(df_counts, values='count', names="shot_type_name", title='Goal Shots')
        display()

    if option == "Shots Outcome":
        df_counts = pd.DataFrame(df["shot_outcome_name"].value_counts())
        df_counts.reset_index(inplace=True)
        fig = px.pie(df_counts, values='count', names='shot_outcome_name', title='Shots Outcome')
        display()

    if option == "Goal":
        df_counts = pd.DataFrame(df["is_goal"].value_counts())
        df_counts.reset_index(inplace=True)
        fig = px.pie(df_counts, values='count', names='is_goal', title='Goal')
        display()



    fig, ax1 = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="is_goal", y="distance_to_goal")
    plt.title("Distance to Goal and Goal Outcome")
    plt.xlabel('is_goal')
    plt.ylabel('distance_to_goal')
    st.pyplot(fig)

if __name__ == "__main__":
    run()