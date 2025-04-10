

def get_name(file_name):
    if 'ins_S' in file_name:
        params = file_name[6:-4].replace('_', ':')
        name = 'ins_S:' + params
    else:
        params = file_name[2:-4].replace('_', ':')
        name = 'S:' + params
    return name


def get_file_name(name):
    if 'ins_S' in name:
        params = name[5:].replace(':', '_')
        name = 'ins_S' + params
    else:
        params = name[1:].replace(':', '_')
        name = 'S' + params
    return name + '.csv'


def is_unknown(name):
    if 'ins_S' in name:
        ins_symbols = name.split(':')[-1]
        return ins_symbols == 'X'
    else:
        return name[-1] == 'X'

def get_position(name):
    if 'ins_S' in name:
        return name.split(':')[-2]
    else:
        if name[-1].isnumeric():
            return name.split(':')[-1]
        else:
            return name.split(':')[1][:-1]

def get_unknown_name(name):
    if 'ins_S' in name:
        return f"ins_S:{get_position(name)}:X"
    else:
        return f"S:{get_position(name)}X"

def get_name_for_URL(name):
    if 'ins_S' in name:
        return f"ins_S{name[5:].replace(':','%3A')}"
    else:
        return name.replace(':','%3A')

def get_aa_parameter(name):
    url_name = get_name_for_URL(name)
    if 'ins_S' in name:
        return f"aminoAcidInsertions={url_name}"
    else:
        return f"aminoAcidMutations={url_name}"


def get_residues(mutations):
    residues = []
    for m in mutations:
        if m[-1].isnumeric():
            residues.append(int(get_position(m)))
    return residues