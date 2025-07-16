import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

def eisenhower_matrix(df):
    st.subheader("🧭 Eisenhower Matrix: Remediation Prioritization")

    required_cols = {'Priority', 'Remediation', 'Urgency', 'Control'}
    if not required_cols.issubset(df.columns):
        st.error(f"Missing columns: {required_cols - set(df.columns)}")
        return

    # Positioning by quadrant
    quadrant_positions = {
        'Do First': (0.25, 0.75),
        'Schedule': (0.25, 0.25),
        'Delegate': (0.75, 0.75),
        'Eliminate': (0.75, 0.25),
    }

    quadrant_colors = {
        'Do First': '#FFCCCC',
        'Schedule': '#FFFACD',
        'Delegate': '#D5F5E3',
        'Eliminate': '#D6EAF8',
    }

    df = df[df['Priority'].isin(quadrant_positions)].copy()
    df['x'] = df['Priority'].apply(lambda p: quadrant_positions[p][0]) + 0.01 * (df.index % 5)
    df['y'] = df['Priority'].apply(lambda p: quadrant_positions[p][1]) + 0.01 * (df.index % 5)

    urgency_color = {'High': 'red', 'Low': 'green'}

    fig = go.Figure()

    # Add quadrants
    for quadrant, (x, y) in quadrant_positions.items():
        x0, y0 = x - 0.25, y - 0.25
        x1, y1 = x + 0.25, y + 0.25
        fig.add_shape(
            type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
            fillcolor=quadrant_colors[quadrant], opacity=0.3, line_width=0
        )
        fig.add_annotation(
            x=x, y=y1 - 0.05,
            text=f"🟦 {quadrant}" if quadrant == "Eliminate" else f"🟥 {quadrant}" if quadrant == "Do First"
            else f"🟨 {quadrant}" if quadrant == "Schedule" else f"🟩 {quadrant}",
            showarrow=False, font=dict(size=14, color="black")
        )

    # Add tasks
    for _, row in df.iterrows():
        label = row['Remediation']
        if len(label) > 40:
            label = label[:40] + "..."
        fig.add_trace(go.Scatter(
            x=[row['x']], y=[row['y']],
            mode="markers+text",
            marker=dict(color=urgency_color.get(row['Urgency'], 'gray'), size=14),
            text=[label],
            textposition="top center",
            hovertext=f"{row['Control']} | {row['Remediation']}",
            hoverinfo="text",
            showlegend=False
        ))

    fig.update_layout(
        title="Eisenhower Matrix for Remediation",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        height=700,
        margin=dict(l=30, r=30, t=60, b=30),
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

