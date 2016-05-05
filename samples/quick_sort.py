with open("data.input") as source_file:
    import pickle
    a_list = pickle.load(source_file)


def quick_sort(seq):
    if len(seq) <= 1:


        return seq
    else:
        pivot = seq[0]
        left = []
        right = []
        for x in seq[1:]:
            if x < pivot:
                left.append(x)
            else:
                right.append(x)


        return quick_sort(left) + [pivot] + quick_sort(right)

result = quick_sort(a_list)

with open("data.output", "w") as output:
    import pickle
    output.write(str(result))