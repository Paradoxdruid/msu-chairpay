#!/usr/bin/env python3
"""Quick Chair Pay Calculator."""

import plotly.graph_objects as go
import plotly.io
import pandas as pd
import streamlit as st

plotly.io.templates.default = "seaborn"

st.title("Chair Pay Calculator")

st.sidebar.header("Variables")

years = int(st.sidebar.number_input("Years Remaining at MSU Denver", value=10))
chair_years = int(st.sidebar.number_input("Years Remaining as Chair", value=6))
base_salary = float(st.sidebar.number_input("Current Base Salary", value=100000))
chair_stipend = float(st.sidebar.number_input("Current Chair Stipend", value=30000))
NEW_STIPEND = 28500


def calculate(years, chair_years, base_salary, chair_stipend, NEW_STIPEND):
    years_list = list(range(2021, 2021 + years))
    five_sixths = (5 / 6) * (base_salary + chair_stipend)
    current = ([base_salary + chair_stipend] * chair_years) + (
        [five_sixths] * (years - chair_years)
    )
    alt = ([base_salary + NEW_STIPEND] * chair_years) + (
        [base_salary] * (years - chair_years)
    )

    cur_df = pd.DataFrame.from_dict({"years": years_list, "Salary": current})
    cur_df = cur_df.set_index("years")
    cur_df["cumsum"] = cur_df["Salary"].cumsum()

    alt_df = pd.DataFrame.from_dict({"years": years_list, "Salary": alt})
    alt_df = alt_df.set_index("years")
    alt_df["cumsum"] = alt_df["Salary"].cumsum()

    return cur_df, alt_df


def make_chart(cur_df, alt_df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=cur_df.index, y=cur_df["cumsum"], name="Current"))
    fig.add_trace(go.Bar(x=alt_df.index, y=alt_df["cumsum"], name="Alternative"))
    fig.update_layout(barmode="group", title="Future Cumulative Earnings")

    return fig


cur_df, alt_df = calculate(years, chair_years, base_salary, chair_stipend, NEW_STIPEND)

fig = make_chart(cur_df, alt_df)

st.plotly_chart(fig)
