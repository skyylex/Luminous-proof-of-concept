import pickle

with open("data.input") as source_file:
    a_list = pickle.load(source_file)

def sort(seq):
    L = len(seq)

    for _ in range(L):
        for n in range(1, L):
            prev = n - 1
            if seq[n] < seq [prev]:
                temp = seq[prev]
                seq[prev] = seq[n]
                seq[n] = temp




    return seq

result = sort(a_list)
with open("data.output", "w") as output:
    output.write(str(result))