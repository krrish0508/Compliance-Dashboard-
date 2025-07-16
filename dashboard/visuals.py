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

def eisenhower_matrix(df):
    st.subheader("🧭 Eisenhower Matrix: Remediation Prioritization")

    if 'Priority' not in df.columns or 'Remediation' not in df.columns or 'Urgency' not in df.columns:
        st.warning("Matrix requires 'Priority', 'Remediation', and 'Urgency' columns.")
        return

    # Coordinates for each quadrant
    priority_coords = {
        'Do First': (0, 1),
        'Schedule': (0, 0),
        'Delegate': (1, 1),
        'Eliminate': (1, 0),
    }

    df = df[df['Priority'].isin(priority_coords)].copy()
    df['x'] = df['Priority'].apply(lambda p: priority_coords[p][0])
    df['y'] = df['Priority'].apply(lambda p: priority_coords[p][1])

    # Truncate long remediation text for better layout
    df['Label'] = df['Remediation'].apply(lambda r: r[:50] + '...' if len(r) > 50 else r)

    fig = px.scatter(
        df,
        x='x',
        y='y',
        text='Label',
        color='Urgency',  # Color by Urgency now
        symbol='Priority',  # Shape by Priority (optional visual cue)
        hover_data=['Control', 'Score', 'Priority', 'Remediation'],
        title="Eisenhower Matrix for Remediation",
        labels={'x': '', 'y': ''},
        color_discrete_map={'High': 'red', 'Low': 'green'},
        height=550
    )

    fig.update_traces(marker=dict(size=18), textposition='top center')

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 1],
            ticktext=['Important', 'Not Important'],
            range=[-0.5, 1.5]
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1],
            ticktext=['Not Urgent', 'Urgent'],
            range=[-0.5, 1.5]
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
