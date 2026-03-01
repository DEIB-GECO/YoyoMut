from builtins import sorted

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import matplotlib.cm as cm
import uuid
from utils.lineages import add_lineages
import altair as alt


def show_mutation_data(all_mutations, selected, min_percentage=15):
    fig = go.Figure()

    cmap = cm.get_cmap('Set1')
    colors = [cmap(i) for i in range(9)]
    colors_hex = [
        {"r": r, "g": g, "b": b, "alpha": a}
        for r, g, b, a in colors
    ]

    cmap = cm.get_cmap('Set2')
    colors = [cmap(i) for i in range(8)]
    colors_hex.extend([
        {"r": r, "g": g, "b": b, "alpha": a}
        for r, g, b, a in colors
    ])
    i = 0
    for mutation in selected:
        r = colors_hex[i].get('r')
        g = colors_hex[i].get('g')
        b = colors_hex[i].get('b')
        i += 1
        i = i % len(colors_hex)
        alpha = 0.2  # transparency level

        color = f'rgba({r},{g},{b},{alpha})'
        fig.add_trace(go.Scatter(
            x=all_mutations[mutation]['data']['start-date'].tolist()
              + all_mutations[mutation]['data']['start-date'][::-1].tolist(),  # forward + reverse for filling
            y=all_mutations[mutation]['data']['ci-upper-avg'].tolist()
              + all_mutations[mutation]['data']['ci-lower-avg'][::-1].tolist(),  # upper then lower reversed
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

    mutations = ", ".join(sorted(selected))
    fig.update_layout(
        title=f"Prevalence of mutations over time: {mutations}",
        yaxis=dict(range=[0, 1])
    )

    unique_key = str(uuid.uuid4())
    st.plotly_chart(fig, key=unique_key)

    selected_mutations = {}
    for mutation in selected:
        selected_mutations[mutation] = all_mutations[mutation]

    with st.spinner("Loading additional information..."):
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


def show_yoyo_by_num_of_hills(yoyo_mutations, title):
    hill_counts = [v["hills"].shape[0] for v in yoyo_mutations.values()]

    df = pd.DataFrame({"hill_count": hill_counts})
    df_counts = df.value_counts("hill_count").reset_index(name="mutation_count")

    chart = (
        alt.Chart(df_counts, title=title)
        .mark_bar()
        .encode(
            x=alt.X("hill_count:O", title="Number of hills", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("mutation_count:Q", title="Number of mutations"),
            tooltip=["hill_count", "mutation_count"]
        )
    )

    st.altair_chart(chart, use_container_width=False)

def show_yoyo_by_hill_length(yoyo_mutations, title, bin_size=100):
    all_lengths = []
    for v in yoyo_mutations.values():
        df_hills = v["hills"]
        if "length-days" in df_hills.columns:
            all_lengths.extend(df_hills["length-days"].tolist())

    if not all_lengths:
        st.warning("No hill lengths found in the data.")
        return

    min_len = min(all_lengths)
    max_len = max(all_lengths)
    bins = range(int(min_len), int(max_len) + bin_size, bin_size)

    df = pd.DataFrame({"length": all_lengths})
    df["length_bin"] = pd.cut(df["length"], bins=bins, right=False)

    counts = df["length_bin"].value_counts().reset_index()
    counts.columns = ["length_bin", "count"]
    counts = counts.sort_values("length_bin")

    counts["length_bin_str"] = counts["length_bin"].astype(str)

    chart = (
        alt.Chart(counts, title=title)
        .mark_bar()
        .encode(
            x=alt.X("length_bin_str:O", title=f"Hill length bins (size={bin_size})", axis=alt.Axis(labelAngle=-60),
                    sort=counts["length_bin_str"].tolist()),
            y=alt.Y("count:Q", title="Number of hills"),
            tooltip=["length_bin_str", "count"]
        )
        .properties(width=700, height=400)
    )

    st.altair_chart(chart, use_container_width=True)


def show_yoyo_by_start_date(yoyo_mutations, title):
    first_hill_dates = []
    for mut, v in yoyo_mutations.items():
        df_hills = v["hills"]
        if not df_hills.empty:
            first_date = pd.to_datetime(df_hills["start-date"]).min()
            first_hill_dates.append(first_date)
        else:
            first_hill_dates.append(pd.NaT)

    df_dates = pd.DataFrame({"first_hill_date": first_hill_dates})
    df_dates["month_year"] = df_dates["first_hill_date"].dt.to_period("M").dt.to_timestamp()
    date_counts = df_dates["month_year"].value_counts().reset_index()
    date_counts.columns = ["month_year", "mutation_count"]
    date_counts = date_counts.sort_values("month_year")

    chart = (
        alt.Chart(date_counts, title=title)
        .mark_bar()
        .encode(
            x=alt.X("month_year:T", title="Start of first hill",
                    axis=alt.Axis(format="%b %Y")),  # format as "Jan 2025"
            y=alt.Y("mutation_count:Q", title="Number of mutations"),
            tooltip=["month_year", "mutation_count"]
        )
        .properties(width=700, height=400)
    )

    st.altair_chart(chart, use_container_width=True)
