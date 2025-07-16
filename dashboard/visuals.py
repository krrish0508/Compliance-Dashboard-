import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import textwrap

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

def wrap_text(text, width=35):
    return "<br>".join(textwrap.wrap(text, width=width))

def eisenhower_matrix(df):
    st.subheader("🧭 Eisenhower Matrix: Remediation Prioritization")

    if 'Priority' not in df.columns or 'Remediation' not in df.columns:
        st.warning("Matrix requires 'Priority' and 'Remediation' columns.")
        return

    quadrant_coords = {
        'Do First': (0.25, 0.75),
        'Delegate': (0.75, 0.75),
        'Schedule': (0.25, 0.25),
        'Eliminate': (0.75, 0.25),
    }

    # Prepare quadrant remediation texts
    grouped = df[df['Priority'].isin(quadrant_coords)].groupby('Priority')['Remediation'].apply(list)

    fig = go.Figure()

    # Draw background quadrants
    fig.add_shape(type="rect", x0=0, y0=0.5, x1=0.5, y1=1, fillcolor="#FF6961", opacity=0.25, line_width=0)  # Do First
    fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=1, y1=1, fillcolor="#77DD77", opacity=0.25, line_width=0)  # Delegate
    fig.add_shape(type="rect", x0=0, y0=0, x1=0.5, y1=0.5, fillcolor="#FFD700", opacity=0.25, line_width=0)  # Schedule
    fig.add_shape(type="rect", x0=0.5, y0=0, x1=1, y1=0.5, fillcolor="#ADD8E6", opacity=0.25, line_width=0)  # Eliminate

    # Add all remediations as wrapped text blocks in each quadrant
    for quadrant, (x, y) in quadrant_coords.items():
        remediations = grouped.get(quadrant, [])
        if remediations:
            wrapped = [wrap_text(item, width=35) for item in remediations]
            full_text = "<br><br>".join(wrapped)  # Add padding
            fig.add_annotation(
                x=x, y=y,
                text=full_text,
                showarrow=False,
                font=dict(size=12, color="black"),
                align="left",
                xanchor="center",
                yanchor="middle"
            )

    # Add quadrant titles
    fig.add_annotation(x=0.25, y=0.97, text="🟥 Do First", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=0.75, y=0.97, text="🟩 Delegate", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=0.25, y=0.03, text="🟨 Schedule", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=0.75, y=0.03, text="🟦 Eliminate", showarrow=False, font=dict(size=14, color="black"))

    fig.update_layout(
        title="Eisenhower Matrix for Remediation",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        height=700,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
