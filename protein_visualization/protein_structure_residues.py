def get_residue_number_adjustments():
    return {
        'N - N ter': {
            'gene': 'N',
            'start': 0,
            'end': 173
        },
        'NSP2': {
            'gene': 'ORF1a',
            'start': 181,
            'end': 818
        },
        'NSP3': {
            'gene': 'ORF1a',
            'start': 1564,
            'end': 1878
        },
        'NSP5': {
            'gene': 'ORF1a',
            'start': 3264,
            'end': 3569
        },
        'NSP9': {
            'gene': 'ORF1a',
            'start': 4140,
            'end': 4253
        },
        'NSP10': {
            'gene': 'ORF1a',
            'start': 4254,
            'end': 4375
        },
        'NSP13': {
            'gene': 'ORF1b',
            'start': 924,
            'end': 1524
        },
        'NSP15':  {
            'gene': 'ORF1b',
            'start': 2051,
            'end': 2399
        },
    }

def adjust_residue_numbers(list_of_residues, protein_structure):
    residue_number_adjustments = get_residue_number_adjustments()

    if protein_structure not in residue_number_adjustments:
        return list_of_residues

    adjusted_residues = []
    range_start = residue_number_adjustments[protein_structure]['start']
    range_end = residue_number_adjustments[protein_structure]['end']
    for resi in list_of_residues:
        if range_start <= int(resi) <= range_end:
            adjusted_residues.append(str(int(resi) - (range_start - 1)))
    return adjusted_residues

def adjust_potential_residues(list_of_potential_residues, protein_structure):
    residue_number_adjustments = get_residue_number_adjustments()

    if protein_structure not in residue_number_adjustments:
        return list_of_potential_residues

    adjusted_residues = {}
    range_start = residue_number_adjustments[protein_structure]['start']
    range_end = residue_number_adjustments[protein_structure]['end']
    for resi in list_of_potential_residues:
        if range_start <= int(resi) <= range_end:
            potential_residue_string = list_of_potential_residues[resi]
            adjusted_residues.update({str(int(resi) - (range_start - 1)): potential_residue_string})
    return adjusted_residues
