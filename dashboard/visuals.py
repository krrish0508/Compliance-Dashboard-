import streamlit as st
import pandas as pd
import plotly.express as px

def radar_chart(df):
    radar_data = df.groupby("Domain")["Score"].mean().reset_index()
    fig = px.line_polar(radar_data, r="Score", theta="Domain", line_close=True,
                        title="Average Score by Domain", markers=True)
    st.plotly_chart(fig, use_container_width=True)

def heatmap(df):
    heat_data = df.pivot_table(index="Domain", columns="Framework", values="Score", aggfunc="mean")
    fig = px.imshow(heat_data, text_auto=True, color_continuous_scale="Blues",
                    title="Domain vs Framework Heatmap")
    st.plotly_chart(fig, use_container_width=True)