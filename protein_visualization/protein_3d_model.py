import html
import json

import streamlit as st

def show_3d_protein(yo_yo_residues, fixated_residues):

    pdb_file_path = "./protein_visualization/SPIKE_WT_NoGLYC_NoH.pdb"
    with open(pdb_file_path, "r") as file:
        pdb_data = file.read()

    pdb_data_safe = html.escape(pdb_data)

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
                highlight_color_fixated = st.color_picker("Select Highlight Color for Fixated residues", "#008000")

            st.divider()
            submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.submitted_3d_form = True
    if st.session_state.get("submitted_3d_form"):
        potentialResi = json.dumps(st.session_state.potential_residues)

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
              let potentialResi = {potentialResi}
        
          
              viewer.addModel(pdbData, "pdb");  // Load PDB from string
              viewer.setStyle({{}}, {{{style}: {{color: '{model_color}'}}}});
        
              
              
              // Color residues by position from the Python list
              let residuePositions_yo_yo = {yo_yo_residues};  // Residue positions from Python
            
              // Loop over the residues and apply a different color
              residuePositions_yo_yo.forEach(function(residueIndex) {{
                viewer.setStyle({{resi: residueIndex}}, {{{yo_yo_style}: {{color: '{highlight_color_yo_yo}'}}}});  // Color the residue
                }});
                // Color residues by position from the Python list
              let residuePositions_fixated = {fixated_residues};  // Residue positions from Python
            
              // Loop over the residues and apply a different color
              residuePositions_fixated.forEach(function(residueIndex) {{
                viewer.setStyle({{resi: residueIndex}}, {{{fixated_style}: {{color: '{highlight_color_fixated}'}}}});  // Color the residue
                }});
        
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
                        let residuePositions_yo_yo = {yo_yo_residues};  // Residue positions from Python
            
                      // Loop over the residues and apply a different color
                      residuePositions_yo_yo.forEach(function(residueIndex) {{
                        viewer.setStyle({{resi: residueIndex}}, {{{yo_yo_style}: {{color: '{highlight_color_yo_yo}'}}}});  // Color the residue
                        }});
                        // Color residues by position from the Python list
                      let residuePositions_fixated = {fixated_residues};  // Residue positions from Python
                    
                      // Loop over the residues and apply a different color
                      residuePositions_fixated.forEach(function(residueIndex) {{
                        viewer.setStyle({{resi: residueIndex}}, {{{fixated_style}: {{color: '{highlight_color_fixated}'}}}});  // Color the residue
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
