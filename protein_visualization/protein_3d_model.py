import html
import json

import streamlit as st

names_dict = {
    "base": "Base",
    "yo_yo": "Yo-yo residues",
    "fixated": "Fixated residues",
    "ss": "SS domain",
    "ntd": "NTD domain",
    "n2r": "N2R domain",
    "rbd": "RBD domain",
    "agss": "Antigenic supersite"
}

# SS (1-26), NTD (residues 27-292), N2R (293-330), and RBD (331-541), antigenic supersite (14-20 + 140-158 + 245-264)
resi_dict = {
    "base": [],
    "yo_yo": [],
    "fixated": [],
    "ss": list(range(1, 27)),
    "ntd": list(range(27, 293)),
    "n2r": list(range(293, 331)),
    "rbd": list(range(331, 542)),
    "agss": list(range(14, 21)) + list(range(140, 159)) + list(range(245 - 265))
}


def get_colors_for_legend():
    keys = ["base", "yo_yo", "fixated", "ss", "ntd", "n2r", "rbd", "agss"]

    color_style_info = {}
    for k in keys:
        if st.session_state.get(f"show_{k}") == "Yes":
            color_style_info.update(
                {k: {"name": names_dict.get(k),
                     "color": st.session_state.get(f"{k}_color"),
                     "style": st.session_state.get(f"{k}_style"),
                     "resi": resi_dict[k]
                     }})
    return color_style_info


def get_domain_html(data):
    html_string = f""
    for k in data:
        if k in ["base", "yo_yo", "fixated"]:
            continue
        html_string += f"""
            let {k}_domain = {data[k]['resi']};  // Get the residue list from Python 
            {k}_domain.forEach(function(residueIndex) {{
                // Apply the style and color to the residues
                viewer.setStyle({{resi: residueIndex}}, {{{data[k]["style"]}: {{color: '{data[k]["color"]}'}}}});  
            }});
            
        """
    return html_string

def collapse_form():
    st.session_state.visualization_form_expanded = False

def show_3d_protein(yo_yo_residues, fixated_residues):
    pdb_file_path = "./protein_visualization/SPIKE_WT_NoGLYC_NoH.pdb"
    with open(pdb_file_path, "r") as file:
        pdb_data = file.read()

    pdb_data_safe = html.escape(pdb_data)
    if 'visualization_form_expanded' not in st.session_state:
        st.session_state.visualization_form_expanded = True
    with st.expander("Advanced visualization options:", expanded=st.session_state.visualization_form_expanded):
        with st.form("3d_model", enter_to_submit=False):
            style_choices = ['sphere', 'stick', 'line', 'cross', 'cartoon']

            model_col1, model_col2 = st.columns(2)
            with model_col1:
                # style = st.radio("Choose the style of the protein model:", style_choices)
                style = st.segmented_control("Choose the style of the protein model:", style_choices,
                                             selection_mode="single",
                                             default="sphere",
                                             key="base_style")
            with model_col2:
                model_color = st.color_picker("Select the color for the protein model", "#808080",
                                              key="base_color")
            st.session_state.show_base = "Yes"
            st.divider()
            yo_yo_col1, yo_yo_col2 = st.columns(2)

            with yo_yo_col1:
                yo_yo_style = st.segmented_control("Choose the style of the yo-yo residues:", style_choices,
                                                   selection_mode="single",
                                                   default="sphere",
                                                   key="yo_yo_style")

            with yo_yo_col2:
                highlight_color_yo_yo = st.color_picker("Select the color for yo-yo residues", "#FF0000",
                                                        key="yo_yo_color")
            st.session_state.show_yo_yo = "Yes"
            st.divider()

            fixated_col1, fixated_col2 = st.columns(2)

            with fixated_col1:
                fixated_style = st.segmented_control("Choose the style of the fixated residues:", style_choices,
                                                     selection_mode="single",
                                                     default="sphere",
                                                     key="fixated_style")

            with fixated_col2:
                highlight_color_fixated = st.color_picker("Select the color for fixated residues", "#008000",
                                                          key="fixated_color")
            st.session_state.show_fixated = "Yes"
            st.divider()

            # domains: SS (1-26), NTD (residues 27-292), N2R (293-330), and RBD (331-541)
            ss_col1, ss_col2, ss_col3 = st.columns([1, 1.5, 2])
            with ss_col1:
                st.radio("Highlight SS domain (1-26):", ['Yes', 'No'], horizontal=True, index=1,
                         key="show_ss")
                # show_ss = st.toggle("Highlight SS domain (1-26):", key="show_ss")
            with ss_col2:
                st.segmented_control("Choose the style of the SS domain:", style_choices,
                                     selection_mode="single",
                                     default="sphere",
                                     key="ss_style")

            with ss_col3:
                st.color_picker("Select the color for the SS domain", "#808080",
                                key="ss_color")
            st.divider()

            ntd_col1, ntd_col2, ntd_col3 = st.columns([1, 1.5, 2])
            with ntd_col1:
                st.radio("Highlight NTD domain (27-292):", ['Yes', 'No'], horizontal=True, index=1,
                         key="show_ntd")

            with ntd_col2:
                st.segmented_control("Choose the style of the NTD domain:", style_choices,
                                     selection_mode="single",
                                     default="sphere",
                                     key="ntd_style")
            with ntd_col3:
                st.color_picker("Select the color for the NTD domain", "#808080",
                                key="ntd_color")

            st.divider()

            n2r_col1, n2r_col2, n2r_col3 = st.columns([1, 1.5, 2])
            with n2r_col1:
                st.radio("Highlight N2R domain (293-330):", ['Yes', 'No'], horizontal=True, index=1,
                         key="show_n2r")
            with n2r_col2:
                st.segmented_control("Choose the style of the N2R domain:", style_choices,
                                     selection_mode="single",
                                     default="sphere",
                                     key="n2r_style")
            with n2r_col3:
                st.color_picker("Select the color for the N2R domain", "#808080",
                                key="n2r_color")

            st.divider()

            rbd_col1, rbd_col2, rbd_col3 = st.columns([1, 1.5, 2])
            with rbd_col1:
                st.radio("Highlight RBD domain (331-541):", ['Yes', 'No'], horizontal=True, index=1,
                         key="show_rbd")
            with rbd_col2:
                st.segmented_control("Choose the style of the RBD domain:", style_choices,
                                     selection_mode="single",
                                     default="sphere",
                                     key="rbd_style")
            with rbd_col3:
                st.color_picker("Select the color for the RBD domain", "#808080",
                                key="rbd_color")

            st.divider()

            antigenic_supersite_col1, antigenic_supersite_col2, antigenic_supersite_col3 = st.columns([1, 1.5, 2])
            with antigenic_supersite_col1:
                st.radio("Highlight antigenic supersite (14-20 + 140-158 + 245-264):",
                         ['Yes', 'No'], horizontal=True, index=1,
                         key="show_agss")
            with antigenic_supersite_col2:
                st.segmented_control("Choose the style of the antigenic supersite:",
                                     style_choices,
                                     selection_mode="single",
                                     default="sphere",
                                     key="agss_style")
            with antigenic_supersite_col3:
                st.color_picker("Select the color for antigenic supersite",
                                "#808080",
                                key="agss_color")

            st.divider()

            submitted = st.form_submit_button("Submit", on_click=collapse_form)

    if submitted:
        st.session_state.submitted_3d_form = True

    if st.session_state.get("submitted_3d_form"):
        # HTML for the 3D model color legend
        visualization_data = get_colors_for_legend()
        columns = st.columns(len(visualization_data))

        for col, k in zip(columns, visualization_data.keys()):
            name = visualization_data.get(k).get("name")
            color = visualization_data.get(k).get("color")
            col.markdown(f"""
                <div style='display: flex; align-items: center; height: 50px;'>
                    <div style='width: 30px; height: 30px; background-color: {color}; margin-right: 6px; border: 1px solid #000;'></div>
                    <span>{name}</span>
                </div>
            """, unsafe_allow_html=True)

        domain_coloring_html = get_domain_html(visualization_data)

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
        
                viewer.addModel(pdbData, "pdb");  // Load PDB from string
                viewer.setStyle({{}}, {{{style}: {{color: '{model_color}'}}}});
        
                {domain_coloring_html}
                
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
                            
                            {domain_coloring_html}
                              
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
