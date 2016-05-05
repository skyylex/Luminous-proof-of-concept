with open("data.input") as source_file:
    import pickle
    a_list = pickle.load(source_file)


def insertion_sort(seq):
    for n in range(1, len(seq)):
        item = seq[n]
        hole = n
        while hole > 0 and seq[hole - 1] > item:
            seq[hole] = seq[hole - 1]
            hole = hole - 1
        seq[hole] = item


    return seq

result = insertion_sort(a_list)

with open("data.output", "w") as output:
    import pickle
    output.write(str(result))
