import random
import time

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import uuid
from utils.lineages import add_lineages

@st.cache_data
def show_mutation_data(all_mutations, selected, min_percentage=15):
    print('started show_mutation_data')
    fig = go.Figure()

    for mutation in selected:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        alpha = 0.2  # transparency level

        color = f'rgba({r},{g},{b},{alpha})'
        fig.add_trace(go.Scatter(
            x=all_mutations[mutation]['data']['start-date'].tolist()
              + all_mutations[mutation]['data']['start-date'][::-1].tolist(),  # forward + reverse for filling
            y=all_mutations[mutation]['data']['ci-upper-avg'].tolist() + all_mutations[mutation]['data']['ci-lower-avg'][::-1].tolist(),  # upper then lower reversed
            fill='toself',
            fillcolor=color,  # semi-transparent fill
            line=dict(color=color),  # no line
            hoverinfo="skip",
            showlegend=True,
            name=f'{mutation} 95% CI'
        ))
        fig.add_trace((go.Scatter(
            x=all_mutations[mutation]['data']['start-date'],
            y=all_mutations[mutation]['data']['avg-proportion'],
            mode='lines+markers',
            name=mutation,
            line=dict(color=f'rgba({r},{g},{b},1)')
        )))

    fig.update_layout(
        title="Sequences over time",
        yaxis=dict(range=[0, 1])
    )

    unique_key = str(uuid.uuid4())
    st.plotly_chart(fig, key=unique_key)

    selected_mutations = {}
    for mutation in selected:
        selected_mutations[mutation] = all_mutations[mutation]
    add_lineages(selected_mutations)


    for mutation in selected:
        with st.expander(f"**{mutation}**"):
            st.write(f"- classified as: *{all_mutations[mutation]['class']}*")

            if not all_mutations[mutation]['hills'].empty:
                st.dataframe(all_mutations[mutation]['hills'],
                             column_config={
                                 "start-date": "Start date",
                                 "end-date": "End date",
                                 "length-days": "Length (in days)"
                             },
                             hide_index=True)
                for i in range(len(all_mutations[mutation]['hills'])):
                    start_date = all_mutations[mutation]['hills'].iloc[i]['start-date']
                    end_date = all_mutations[mutation]['hills'].iloc[i]['end-date']
                    if end_date is None:
                        end_date = 'today'
                    st.write(f"- most prevalent lineages for **{mutation}** -> **{start_date} - {end_date}**:")
                    st.dataframe(all_mutations[mutation]['lineages'][start_date],
                                 hide_index=True,
                                 column_order=("Lineages (aliases)", "Proportion"),
                                 column_config={
                                    "Proportion": st.column_config.NumberColumn(format="%.2f%%")
                                 })
