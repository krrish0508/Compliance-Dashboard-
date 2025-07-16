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

    if 'Priority' not in df.columns or 'Remediation' not in df.columns or 'Urgency' not in df.columns:
        st.warning("Matrix requires 'Priority', 'Remediation', and 'Urgency' columns.")
        return

    priority_coords = {
        'Do First': (0.25, 0.75),
        'Schedule': (0.25, 0.25),
        'Delegate': (0.75, 0.75),
        'Eliminate': (0.75, 0.25),
    }

    df = df[df['Priority'].isin(priority_coords)].copy()
    df['x'] = df['Priority'].apply(lambda p: priority_coords[p][0]) + 0.01 * (df.index % 5)
    df['y'] = df['Priority'].apply(lambda p: priority_coords[p][1]) + 0.01 * (df.index % 5)

    urgency_colors = {'High': 'red', 'Low': 'green'}

    fig = go.Figure()

    # Quadrant backgrounds
    fig.add_shape(type="rect", x0=0, y0=0.5, x1=0.5, y1=1, fillcolor="#ffcccc", opacity=0.3, line_width=0)
    fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=1, y1=1, fillcolor="#c6f6c6", opacity=0.3, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=0, x1=0.5, y1=0.5, fillcolor="#fff6b2", opacity=0.3, line_width=0)
    fig.add_shape(type="rect", x0=0.5, y0=0, x1=1, y1=0.5, fillcolor="#cce5ff", opacity=0.3, line_width=0)

    # Plot visible text and points
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['x']],
            y=[row['y']],
            mode='markers+text',
            marker=dict(size=14, color=urgency_colors.get(row['Urgency'], 'gray')),
            text=[row['Remediation'][:45] + '...' if len(row['Remediation']) > 45 else row['Remediation']],
            textposition='bottom center',
            hovertext=f"{row['Control']} ({row['Priority']}, {row['Urgency']}): {row['Remediation']}",
            hoverinfo="text",
            showlegend=False
        ))

    # Quadrant titles
    fig.add_annotation(x=0.25, y=0.95, text="🔴 Do First", showarrow=False, font=dict(size=14))
    fig.add_annotation(x=0.75, y=0.95, text="🟢 Delegate", showarrow=False, font=dict(size=14))
    fig.add_annotation(x=0.25, y=0.05, text="🟡 Schedule", showarrow=False, font=dict(size=14))
    fig.add_annotation(x=0.75, y=0.05, text="🔵 Eliminate", showarrow=False, font=dict(size=14))

    fig.update_layout(
        title="Eisenhower Matrix for Remediation",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        height=650,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

