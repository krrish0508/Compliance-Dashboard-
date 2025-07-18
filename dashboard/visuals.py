import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import textwrap

# Radar chart function
def radar_chart(df):
    radar_data = df.groupby("Domain")["Score"].mean().reset_index()
    fig = px.line_polar(radar_data, r="Score", theta="Domain", line_close=True,
                        title="Average Score by Domain", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# Heatmap function
def heatmap(df):
    heat_data = df.pivot_table(index="Domain", columns="Framework", values="Score", aggfunc="mean")
    fig = px.imshow(heat_data, text_auto=True, color_continuous_scale="Blues",
                    title="Domain vs Framework Heatmap")
    st.plotly_chart(fig, use_container_width=True)

# Text wrapping helper
def wrap_text(text, width=35):
    return "<br>".join(textwrap.wrap(text, width=width))

# Eisenhower Matrix
def eisenhower_matrix(df):
    st.subheader("🧭 Eisenhower Matrix: Remediation Prioritization")

    required_cols = ['Priority', 'Remediation', 'Domain', 'Control']
    if not all(col in df.columns for col in required_cols):
        st.warning(f"Matrix requires columns: {', '.join(required_cols)}")
        return

    quadrant_coords = {
        'Do First': (0.25, 0.75),
        'Delegate': (0.75, 0.75),
        'Schedule': (0.25, 0.25),
        'Eliminate': (0.75, 0.25),
    }

    df = df[df['Priority'].isin(quadrant_coords)].copy()

    # Formatted string: [Domain] (Control) Remediation
    df['Formatted'] = df.apply(lambda row: f"[{row['Domain']}] ({row['Control']}) {row['Remediation']}", axis=1)
    grouped = df.groupby('Priority')['Formatted'].apply(list)

    fig = go.Figure()

    # Add quadrant backgrounds
    fig.add_shape(type="rect", x0=0, y0=0.5, x1=0.5, y1=1, fillcolor="#FF6961", opacity=0.25, line_width=0)  # Do First
    fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=1, y1=1, fillcolor="#77DD77", opacity=0.25, line_width=0)  # Delegate
    fig.add_shape(type="rect", x0=0, y0=0, x1=0.5, y1=0.5, fillcolor="#FFD700", opacity=0.25, line_width=0)  # Schedule
    fig.add_shape(type="rect", x0=0.5, y0=0, x1=1, y1=0.5, fillcolor="#ADD8E6", opacity=0.25, line_width=0)  # Eliminate

    # Add remediation texts
    for priority, (x, y) in quadrant_coords.items():
        items = grouped.get(priority, [])
        if items:
            wrapped_text = "<br><br>".join([wrap_text(i, width=35) for i in items])
            fig.add_annotation(
                x=x, y=y,
                text=wrapped_text,
                showarrow=False,
                font=dict(size=12, color="black"),
                align="left",
                xanchor="center",
                yanchor="middle"
            )

    # Quadrant labels
    fig.add_annotation(x=0.25, y=0.97, text="🟥 Do First", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=0.75, y=0.97, text="🟩 Delegate", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=0.25, y=0.03, text="🟨 Schedule", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=0.75, y=0.03, text="🟦 Eliminate", showarrow=False, font=dict(size=14, color="black"))

    fig.update_layout(
        title="Eisenhower Matrix for Remediation",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        height=720,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
