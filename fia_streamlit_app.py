import pandas as pd

# Polyfill for pandas.DataFrame.append (for Pandas >=2.0)
if not hasattr(pd.DataFrame, "append"):
    def _append(self, other, ignore_index=False, **kwargs):
        return pd.concat([self, other], ignore_index=ignore_index)
    pd.DataFrame.append = _append

import streamlit as st
import plotly.graph_objs as go
import plotly.express as px

# Page layout
st.set_page_config(page_title="Player-Type Semantic Dashboard", layout="wide")

# 1) Define all 28 traits
traits = [
    "Accountability","Attachment","Boundary Violations","Charm","Cognitive Flexibility",
    "Conflict","Control","Deception","Disrespect","Dominance","Dysregulation",
    "Emotional Over-Exposure","Empathy","Enmeshment","Exploitation","Grandiosity",
    "Hyperlogical Thinking","Impulsivity","Inconsistency","Intensity","Isolation",
    "Neediness","Perseveration","Respect","Sensation-Seeking","Sense of Self",
    "Superficiality","Trust","Validation-Seeking"
]

# 2) High/Low mappings
high_map = {
    "The Puppet Master":       ["Exploitation","Deception","Charm"],
    "The Intimidator":         ["Control","Boundary Violations","Dominance"],
    "The Self-Obsessed":       ["Grandiosity","Validation-Seeking","Superficiality"],
    "The Drill Sergeant":      ["Control","Dominance","Sense of Self"],
    "The Suspicious Strategist":["Isolation","Conflict","Control"],
    "Master of Everything":    ["Dominance","Conflict","Grandiosity"],
    "The Subtle Saboteur":     ["Disrespect","Inconsistency","Control"],
    "The Clinger":             ["Enmeshment","Dysregulation","Attachment"],
    "The Addict":              ["Dysregulation","Impulsivity","Inconsistency"],
    "The Parental Seeker":     ["Neediness","Charm","Attachment"],
    "The Future Faker":        ["Deception","Inconsistency","Superficiality"],
    "The Freewheeler":         ["Impulsivity","Hyperlogical Thinking","Sensation-Seeking"],
    "The Thinker":             ["Cognitive Flexibility","Perseveration","Trust"],
    "Emotional Invalidator":   ["Disrespect","Grandiosity","Dominance"],
    "The Emotionally Distant": ["Inconsistency","Superficiality","Control"],
    "The Rake":                ["Charm","Sensation-Seeking","Intensity"],
    "The Perpetual Victim":    ["Validation-Seeking","Inconsistency","Emotional Over-Exposure"]
}
low_map = {
    "The Puppet Master":       ["Sense of Self","Attachment","Accountability"],
    "The Intimidator":         ["Empathy","Accountability","Neediness"],
    "The Self-Obsessed":       ["Trust","Empathy","Accountability"],
    "The Drill Sergeant":      ["Neediness","Emotional Over-Exposure","Hyperlogical Thinking"],
    "The Suspicious Strategist":["Trust","Charm","Cognitive Flexibility"],
    "Master of Everything":    ["Enmeshment","Neediness","Accountability"],
    "The Subtle Saboteur":     ["Dysregulation","Conflict","Accountability"],
    "The Clinger":             ["Sense of Self","Disrespect","Grandiosity"],
    "The Addict":              ["Sense of Self","Control","Accountability"],
    "The Parental Seeker":     ["Dominance","Perseveration","Accountability"],
    "The Future Faker":        ["Attachment","Perseveration","Empathy"],
    "The Freewheeler":         ["Control","Dominance","Cognitive Flexibility"],
    "The Thinker":             ["Impulsivity","Charm","Sensation-Seeking"],
    "Emotional Invalidator":   ["Attachment","Empathy","Enmeshment"],
    "The Emotionally Distant": ["Enmeshment","Dysregulation","Attachment"],
    "The Rake":                ["Attachment","Accountability","Sense of Self"],
    "The Perpetual Victim":    ["Accountability","Empathy","Perseveration"]
}

# 3) Build DataFrame and long format
rows = []
for ptype in high_map:
    scores = [5]*len(traits)
    for h in high_map[ptype]:
        scores[traits.index(h)] = 10
    for l in low_map[ptype]:
        scores[traits.index(l)] = 2
    rows.append([ptype] + scores)
df = pd.DataFrame(rows, columns=["Type"]+traits)
df_long = df.melt(id_vars="Type", var_name="Trait", value_name="Score")

# 4) Pre-assign colors
palette = px.colors.qualitative.Plotly
colors = palette * 2
color_map = {ptype: colors[i] for i, ptype in enumerate(high_map.keys())}

# 5) UI with adjusted column widths
st.title("🎲 Player-Type Semantic Dashboard")
side, main = st.columns([1, 6])  # smaller side panel, larger main area

with side:
    selected = st.multiselect(
        "Select player types:",
        options=list(high_map.keys()),
        default=["The Puppet Master"]
    )

with main:
    if not selected:
        st.warning("Pick at least one type.")
    else:
        fig = go.Figure()
        for p in selected:
            d = df_long[df_long["Type"]==p]
            fig.add_trace(go.Scatterpolar(
                r=d["Score"], theta=d["Trait"],
                fill="toself", name=p,
                line_color=color_map[p]
            ))
        # Make graph bigger
        fig.update_layout(
            width=900, height=700,
            polar=dict(
                radialaxis=dict(visible=False),
                angularaxis=dict(tickfont=dict(size=10))
            ),
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5
            ),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)