import html
import json

import streamlit as st

def show_3d_protein(yo_yo_residues, fixated_residues):

    pdb_file_path = "./protein_visualization/SPIKE_WT_NoGLYC_NoH.pdb"
    # pdb_file_path = "./protein_visualization/SPIKE_short.pdb"
    with open(pdb_file_path, "r") as file:
        pdb_data = file.read()

    pdb_data_safe = html.escape(pdb_data)

    # SS (1-26), NTD (residues 27-292), N2R (293-330), and RBD (331-541), antigenic supersite (14-20 + 140-158 + 245-264)
    ss = list(range(1, 27))
    ntd = list(range(27, 293))
    n2r = list(range(293, 331))
    rbd = list(range(331, 542))
    agss = list(range(14, 21)) + list(range(140, 159)) + list(range(245-265))


    with st.expander("Customize visualization:", expanded=True):
        with st.form("3d_model", enter_to_submit=False):
            style_choices = ['sphere', 'stick', 'line', 'cross', 'cartoon']

            model_col1, model_col2 = st.columns(2)
            with model_col1:
                style = st.radio("Choose the style of the protein model:", style_choices)
            with model_col2:
                model_color = st.color_picker("Select the color for the protein model", "#808080")

            st.divider()
            yo_yo_col1, yo_yo_col2 = st.columns(2)

            with yo_yo_col1:
                yo_yo_style = st.radio("Choose the style of the yo-yo residues:", style_choices)

            with yo_yo_col2:
                highlight_color_yo_yo = st.color_picker("Select the color for yo-yo residues", "#FF0000")

            st.divider()

            fixated_col1, fixated_col2 = st.columns(2)

            with fixated_col1:
                fixated_style = st.radio("Choose the style of the fixated residues:", style_choices)

            with fixated_col2:
                highlight_color_fixated = st.color_picker("Select the color for fixated residues", "#008000")

            st.divider()

            # domains: SS (1-26), NTD (residues 27-292), N2R (293-330), and RBD (331-541)
            show_ss = st.radio("Highlight SS domain (1-26):", ['Yes', 'No'], horizontal=True, index=1)
            ss_col1, ss_col2 = st.columns(2)
            with ss_col1:
                ss_style = st.radio("Choose the style of the SS domain:", style_choices)

            with ss_col2:
                ss_highlight_color = st.color_picker("Select the color for the SS domain", "#808080")

            st.divider()

            show_ntd = st.radio("Highlight NTD domain (27-292):", ['Yes', 'No'], horizontal=True, index=1)
            ntd_col1, ntd_col2 = st.columns(2)
            with ntd_col1:
                ntd_style = st.radio("Choose the style of the NTD domain:", style_choices)

            with ntd_col2:
                ntd_highlight_color = st.color_picker("Select the color for the NTD domain", "#808080")

            st.divider()

            show_n2r = st.radio("Highlight N2R domain (293-330):", ['Yes', 'No'], horizontal=True, index=1)
            n2r_col1, n2r_col2 = st.columns(2)
            with n2r_col1:
                n2r_style = st.radio("Choose the style of the N2R domain:", style_choices)

            with n2r_col2:
                n2r_highlight_color = st.color_picker("Select the color for the N2R domain", "#808080")

            st.divider()

            show_rbd = st.radio("Highlight RBD domain (331-541):", ['Yes', 'No'], horizontal=True, index=1)
            rbd_col1, rbd_col2 = st.columns(2)
            with rbd_col1:
                rbd_style = st.radio("Choose the style of the RBD domain:", style_choices)

            with rbd_col2:
                rbd_highlight_color = st.color_picker("Select the color for the RBD domain", "#808080")

            st.divider()

            show_agss = st.radio("Highlight antigenic supersite (14-20 + 140-158 + 245-264):", ['Yes', 'No'], horizontal=True, index=1)
            antigenic_supersite_col1, antigenic_supersite_col2 = st.columns(2)
            with antigenic_supersite_col1:
                antigenic_supersite_style = st.radio("Choose the style of the antigenic supersite:", style_choices)

            with antigenic_supersite_col2:
                antigenic_supersite_highlight_color = st.color_picker("Select the color for antigenic supersite", "#808080")

            st.divider()

            submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.submitted_3d_form = True
    potentialResi = json.dumps(st.session_state.potential_residues)
    if st.session_state.get("submitted_3d_form"):
        if show_ss == 'No':
            ss = []
        if show_ntd == 'No':
            ntd = []
        if show_n2r == 'No':
            n2r = []
        if show_rbd == 'No':
            rbd = []
        if show_agss == 'No':
            agss =[]


    html_code = f"""
        <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
        <div id="container-01" class="mol-container"></div>
        <style>
            .mol-container {{
              width: 100%;
              height: 800px;
              position: relative;
            }}
        </style>
        <script>
            let element = document.querySelector('#container-01');
            let config = {{ backgroundColor: 'white' }};
            let viewer = $3Dmol.createViewer( element, config );
            let pdbData = `{pdb_data_safe}`;  // Embed PDB data from Python
    
            viewer.addModel(pdbData, "pdb");  // Load PDB from string
            viewer.setStyle({{}}, {{{style}: {{color: '{model_color}'}}}});
    
            let ss_domain = {ss};  // Get the residue list from Python 
            ss_domain.forEach(function(residueIndex) {{
              viewer.setStyle({{resi: residueIndex}}, {{{ss_style}: {{color: '{ss_highlight_color}'}}}});  // Apply the style and color to the residues
              }});
              
            let ntd_domain = {ntd};  
            ntd_domain.forEach(function(residueIndex) {{
              viewer.setStyle({{resi: residueIndex}}, {{{ntd_style}: {{color: '{ntd_highlight_color}'}}}});  
              }});
              
            let n2r_domain = {n2r};  
            n2r_domain.forEach(function(residueIndex) {{
              viewer.setStyle({{resi: residueIndex}}, {{{n2r_style}: {{color: '{n2r_highlight_color}'}}}});  
              }});
              
            let rbd_domain = {rbd};  
            rbd_domain.forEach(function(residueIndex) {{
              viewer.setStyle({{resi: residueIndex}}, {{{rbd_style}: {{color: '{rbd_highlight_color}'}}}});  
              }});
              
            let antigenic_supersite = {agss};  
            antigenic_supersite.forEach(function(residueIndex) {{
              viewer.setStyle({{resi: residueIndex}}, {{{antigenic_supersite_style}: {{color: '{antigenic_supersite_highlight_color}'}}}});
              }});
            
            let residuePositions_yo_yo = {yo_yo_residues};  
            residuePositions_yo_yo.forEach(function(residueIndex) {{
              viewer.setStyle({{resi: residueIndex}}, {{{yo_yo_style}: {{color: '{highlight_color_yo_yo}'}}}});  
              }});
            let residuePositions_fixated = {fixated_residues};  
            residuePositions_fixated.forEach(function(residueIndex) {{
              viewer.setStyle({{resi: residueIndex}}, {{{fixated_style}: {{color: '{highlight_color_fixated}'}}}});  
              }});
    
            let potentialResi = {potentialResi}

            // Hover effect to show residue labels
            let hoverLabel = null;
            viewer.setHoverable({{}}, true, function(atom) {{
                if (atom && atom.resn) {{
                    let potentialResidues = potentialResi[atom.resi] || "No other residues"
                    let labelText = `Residue: ${{atom.resn}} ${{atom.resi}} (${{potentialResidues}})`;
                    if (hoverLabel) viewer.removeLabel(hoverLabel);
                    hoverLabel = viewer.addLabel(labelText, {{
                        position: {{x: atom.x, y: atom.y, z: atom.z}},
                        backgroundColor: 'white',
                        fontSize: 12,
                        fontColor: 'black',
                        edgeWidth: 2,
                        edgeColor: 'black'
                    }});
                }}
            }}, function() {{
                if (hoverLabel) viewer.removeLabel(hoverLabel);
                hoverLabel = null;
            }});
                
            let lastSelected = null; // Track the last clicked residue
      
            viewer.setClickable({{}}, true, function(atom) {{
                if (atom.resi) {{
                    if (lastSelected && lastSelected.resi === atom.resi) {{
                        // If clicking the same residue again, reset view
                        viewer.zoomTo();
                        viewer.setStyle({{}}, {{{style}: {{color: 'grey'}}}});
                        
                        let ss_domain = {ss};  
                        ss_domain.forEach(function(residueIndex) {{
                        viewer.setStyle({{resi: residueIndex}}, {{{ss_style}: {{color: '{ss_highlight_color}'}}}});  
                        }});
                    
                        let ntd_domain = {ntd};  
                        ntd_domain.forEach(function(residueIndex) {{
                            viewer.setStyle({{resi: residueIndex}}, {{{ntd_style}: {{color: '{ntd_highlight_color}'}}}});  
                        }});
                            
                        let n2r_domain = {n2r};  
                        n2r_domain.forEach(function(residueIndex) {{
                            viewer.setStyle({{resi: residueIndex}}, {{{n2r_style}: {{color: '{n2r_highlight_color}'}}}});  
                        }});
                          
                        let rbd_domain = {rbd};  
                        rbd_domain.forEach(function(residueIndex) {{
                            viewer.setStyle({{resi: residueIndex}}, {{{rbd_style}: {{color: '{rbd_highlight_color}'}}}});  
                        }});
                          
                        let antigenic_supersite = {agss};  
                        antigenic_supersite.forEach(function(residueIndex) {{
                            viewer.setStyle({{resi: residueIndex}}, {{{antigenic_supersite_style}: {{color: '{antigenic_supersite_highlight_color}'}}}});
                        }});
                          
                        let residuePositions_yo_yo = {yo_yo_residues};  // Residue positions from Python            
                        residuePositions_yo_yo.forEach(function(residueIndex) {{
                            viewer.setStyle({{resi: residueIndex}}, {{{yo_yo_style}: {{color: '{highlight_color_yo_yo}'}}}});  
                        }});
            
                        let residuePositions_fixated = {fixated_residues};  // Residue positions from Python  
                        residuePositions_fixated.forEach(function(residueIndex) {{
                            viewer.setStyle({{resi: residueIndex}}, {{{fixated_style}: {{color: '{highlight_color_fixated}'}}}});  
                        }});
                        
                        lastSelected = null; // Clear selection
                    }} else {{
                        // Zoom to new residue
                        viewer.zoomTo({{resi: atom.resi, chain: atom.chain}});
                        lastSelected = {{resi: atom.resi, chain: atom.chain}}; // Save selection
                    }}
                    viewer.render();
                }}
            }});
          
            viewer.zoomTo();
            viewer.render();  
        </script>
        """
    st.components.v1.html(html_code, height=800)
