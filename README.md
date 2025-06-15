# YoyoMut

Reversion of amino acid mutations in structural proteins is common in viral evolution. SARS-CoV-2 provides an unprecedented opportunity for ecological studies, thanks to the abundance of available whole genome sequences.

YoyoMut is a tool that allows regular scanning of open SARS-CoV-2 data, reporting on all cyclic and reverting mutations within all proteins (including Spike), with fine-grained trend visualization distinguishing non-mutated from mutated positions (either fixated or cyclically reversed). Classification is determined using alternative algorithms (based on threshold or slope inversion); finally, a 3D-protein structure allows us to identify spatial clustering of adjacent mutated positions.

ℹ️ Disclaimer: Currently only the analysis of the Spike protein is available, others will be added in future updates.

Systematic monitoring of these behaviors relieves a heavy burden on immunologists and structuralists; our tool has practical implications for vaccine and therapeutic anti-Spike monoclonal antibody (mAb) design; attention to cyclic mutation and reversion models could avoid the recent failures in mAb development and inform future strategies.

## Used data
Data is sourced from CoV-Spectrum via Lapis webservice. Files were last-updated on 2025-04-19. Future development will allow updates on a weekly basis.

## App details
The amino acid residues can be classified into three classes: unmutated, yo-yo mutations or fixated mutations. In order to get started, users need to choose certain parameters, such as threshold, duration and minimal lineage percentage, or choose the number of points to use for slope calculation. These parameters affect how the residues, and specific mutations on residues, are classified into the above-mentioned groups.

The classified mutations can be viewed in two ways:

- Mutation classification: shows graphs with relative frequency of mutation at a given amino acid residue in time
- 3D protein model: renders a 3D model of the Spike protein, coloring the residues in different colors depending on their classification
  
To save the results of certain configurations, we are developing a function to print automatic reports. Additional details and instructions can be found in the Help tab.

---

## Acknowledgments

We gratefully acknowledge the authors of CoV-Spectrum and the related LAPIS API, for their help to the community and Chen Chaoran for the support provided to us while developing YoyoMut.

Chen, C., et al. "CoV-Spectrum: Analysis of globally shared SARS-CoV-2 data to Identify and Characterize New Variants" Bioinformatics (2021); 10.1093/bioinformatics/btab856Chen

---

## Contacts

Anna Bernasconi, https://annabernasconi.faculty.polimi.it/

anna.bernasconi@polimi.it, Phone: +39 02 2399 3494

Contributors

- Jana Penic
- Dr. Tommaso Alfonsi
- Prof. Anna Bernasconi

Dipartimento di Elettronica, Informazione e Bioingegneria - Politecnico di Milano
Via Ponzio 34/5 Milano
20133 Milano
Italy

with the collaboration of:

Dr. Daniele Focosi (Pisa University Hospital)

Dr. Fabrizio Maggi (National Institute for Infectious Diseases Lazzaro Spallanzani)

Prof. Giovanni Chillemi (Università della Tuscia)

Dr. Ingrid Guarnetti Prandi (Independent Researcher)
