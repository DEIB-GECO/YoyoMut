import streamlit as st
import sys

sys.path.append("../")

st.set_page_config(page_title="Home page", layout="wide")

if 'not_first_load' not in st.session_state:
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state.not_first_load = True

if 'last_date' not in st.session_state:
    with open("data/metadata/last_date.txt", 'r') as f:
        last_date = f.read()
        st.session_state.last_date = last_date

st.title(f"YoyoMut", anchor=False)

st.write(f"Reversion of amino acid mutations in structural proteins is common in viral evolution. "
         f"SARS-CoV-2 provides an unprecedented opportunity for ecological studies, thanks to the "
         f"abundance of available whole genome sequences.")

st.write(f"**YoyoMut** is a tool that allows regular scanning of open SARS-CoV-2 data, reporting on all **cyclic "
         f"and reverting mutations** within **all proteins (including Spike)**, with fine-grained trend visualization "
         f"distinguishing non-mutated from mutated positions (either fixated or cyclically reversed). "
         f"**Classification** is determined **using alternative algorithms** (based on threshold or slope inversion); "
         f"finally, a **3D-protein structure** allows us to identify **spatial clustering of adjacent mutated "
         f"positions**.")

st.write(f"- **Disclaimer:** Currently only the analysis of the Spike protein is available, others "
         f"will be added in future updates.")

st.write(f"**Systematic monitoring** of these behaviors relieves a heavy burden on immunologists and structuralists; "
         f"our tool has **practical implications for vaccine and therapeutic anti-Spike monoclonal antibody (mAb) "
         f"design;** attention to cyclic mutation and reversion models could avoid the recent failures in mAb "
         f"development and inform future strategies.")

st.write(f"""*Used data*   
        Data is sourced from CoV-Spectrum via 
        [Lapis](https://lapis.cov-spectrum.org/open/v2/docs/getting-started/introduction) 
        webservice. 
        Files were last-updated on {st.session_state.last_date}. 
        Future development will allow updates on a weekly basis.
        """)

st.write(f"""*App details*   
        The amino acid residues can be classified into three classes: *unmutated*, *yo-yo mutations* or *fixated 
        mutations*. In order to get started, users need to choose certain parameters, such as threshold, duration 
        and minimal lineage percentage, or choose the number of points to use for slope calculation. 
        These parameters affect how the residues, and specific mutations on residues, are classified 
        into the above-mentioned groups.
        """)

st.markdown(f"""The classified mutations can be viewed in two ways:  
- **Mutation classification**  
  - shows graphs with relative frequency of mutation at a given amino acid residue in time  
- **3D protein model**  
  - renders a 3D model of the Spike protein, coloring the residues in different colors depending on 
          their classification
""")

st.write(f"""To save the results of certain configurations, we are developing a function to print automatic reports. 
        Additional details and instructions can be found in the Help tab.""")

st.subheader(f"""Acknowledgments""", anchor=False)
st.write(f"""
        We gratefully acknowledge the authors of CoV-Spectrum and the related LAPIS API, for their help to the 
        community and Chen Chaoran for the support provided to us while developing YoyoMut.
        """)
st.write(f"""
        Chen, C., et al. "CoV-Spectrum: Analysis of globally shared SARS-CoV-2 data to Identify and Characterize 
        New Variants" Bioinformatics (2021); 
        [10.1093/bioinformatics/btab856Chen](https://doi.org/10.1093/bioinformatics/btab856)
""")

st.subheader("Contacts", anchor=False)
st.write(f"""
Anna Bernasconi  
[https://annabernasconi.faculty.polimi.it/](https://annabernasconi.faculty.polimi.it/)  
[anna.bernasconi@polimi.it](mailto:anna.bernasconi@polimi.it)  
Phone: [+39 02 2399 3494](tel:+390223993494)  
""")

st.subheader("Contributors", anchor=False)
st.write(f"""
**Jana Penic**  


**Dr. Tommaso Alfonsi**  
**Prof. Anna Bernasconi**  
*Dipartimento di Elettronica, Informazione e Bioingegneria - Politecnico di Milano  
Via Ponzio 34/5 Milano  
20133 Milano  
Italy*  

*with the collaboration of:*

**Dr. Daniele Focosi**  
*Pisa University Hospital*

**Dr. Fabrizio Maggi**  
*National Institute for Infectious Diseases Lazzaro Spallanzani*

**Prof. Giovanni Chillemi**  
*Università della Tuscia*

**Dr. Ingrid Guarnetti Prandi**  
*Independent Researcher* 

""")
