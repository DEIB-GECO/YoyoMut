from datetime import datetime

import streamlit as st

def classify_mutation(df, min_length):
    if 'last_date' not in st.session_state:
        with open("data/metadata/last_date.txt", 'r') as f:
            last_date = f.read()
            st.session_state.last_date = last_date

    if df.shape[0] > 1:
        return 'yo-yo'
    elif df.shape[0] == 1 and df.iloc[0]['end-date'] != None:
        return 'yo-yo'
    elif df.shape[0] == 1 and df.iloc[0]['end-date'] == None:
        date_format = '%Y-%m-%d'
        if (datetime.strptime(st.session_state.last_date, date_format) - datetime.strptime(df.iloc[0]['start-date'],
                                                                         date_format)).days < min_length:
            return 'unclassified'
        else:
            return 'fixated'
    else:
        return 'unclassified'


@st.cache_data
def filter_mutations(mutations):
    import time
    start_time = time.time()
    yo_yo = {}
    fixated = {}
    for mutation in mutations:
        if mutations[mutation]['class'] == 'yo-yo':
            yo_yo.update({mutation: mutations[mutation]})
        elif mutations[mutation]['class'] == 'fixated':
            fixated.update({mutation: mutations[mutation]})
    print("Filtering took:", time.time() - start_time)
    return yo_yo, fixated

