

def generateURL(name):
    # https://open.cov-spectrum.org/explore/World/AllSamples/AllTimes/variants?aaInsertions=ins_s%3A214%3Aepe&
    # https://open.cov-spectrum.org/explore/World/AllSamples/AllTimes/variants?aaMutations=S%3A982A&
    insertion_base = 'https://open.cov-spectrum.org/explore/World/AllSamples/AllTimes/variants?aaInsertions='
    mutation_base = 'https://open.cov-spectrum.org/explore/World/AllSamples/AllTimes/variants?aaMutations='
    if 'ins_S' in name:
        params = name[5:-4].replace('_', '%3A')
        url = insertion_base + 'ins_S%3A' + params
    else:
        params = name[2:-4].replace('_', '%3A')
        url = mutation_base + 'S%3A' + params
    return url