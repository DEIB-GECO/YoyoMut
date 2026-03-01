def get_name(file_name):
    if '.csv' in file_name:
        file_name = file_name.replace('.csv', '')
    if 'ins_' in file_name:
        params = file_name[4:].replace('_', ':')
        name = 'ins_' + params
    else:
        name = file_name.replace('_', ':')
    name = name.replace('Z', '*')
    return name


def get_file_name(name):
    return name.replace(':', '_').replace('*', 'Z') + '.csv'


def is_unknown(name):
    if 'ins_' in name:
        ins_symbols = name.split(':')[-1]
        return ins_symbols == 'X'
    else:
        return name[-1] == 'X'


def get_position(name):
    if 'ins_' in name:
        return name.split(':')[-2]
    else:
        if name[-1].isnumeric():
            return name.split(':')[-1]
        else:
            return name.split(':')[1][:-1]


def get_unknown_name(name):
    if 'ins_' in name:
        protein = name.split(':')[0].split('_')[-1]
        return f"ins_{protein}:{get_position(name)}:X"
    else:
        protein = name.split(':')[0]
        return f"{protein}:{get_position(name)}X"


def get_name_for_URL(name):
    if 'ins_' in name:
        return f"ins_{name[4:].replace(':', '%3A')}"
    else:
        return name.replace(':', '%3A')


def get_aa_parameter(name):
    url_name = get_name_for_URL(name)
    if 'ins_' in name:
        return f"aminoAcidInsertions={url_name}"
    else:
        return f"aminoAcidMutations={url_name}"


def get_positions(mutations):
    residues = []
    for m in mutations:
        if m[-1].isnumeric():
            residues.append(int(get_position(m)))
    return residues


def get_aa_name(residue):
    if 'ins_' in residue:
        return residue.split(':')[-1]
    else:
        return residue.split(get_position(residue))[-1]


def get_protein_name(mutation):
    protein_name = mutation.split(':')[0]
    if 'ins_' in protein_name:
        return protein_name.split('_')[-1]
    else:
        return protein_name
