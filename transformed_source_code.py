file_descriptor = open("data_collection.txt", "w")

a_list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
file_descriptor.write("[var_change] " + "a_list =" + str(a_list) + "\n")


def merge_sort(a):
    file_descriptor.write("[stack_trace]" + str(traceback.extract_stack()) + "\n")
    file_descriptor.write("[var_change] " + "a =" + str(a) + "\n")

    print("Splitting ", a)
    if len(a) > 1:
        mid = len(a) // 2
        file_descriptor.write("[var_change] " + "mid =" + str(mid) + "\n")

        left_half = a[:mid]
        file_descriptor.write("[var_change] " + "left_half =" + str(left_half) + "\n")

        right_half = a[mid:]
        file_descriptor.write("[var_change] " + "right_half =" + str(right_half) + "\n")


        merge_sort(left_half)
        merge_sort(right_half)

        i = 0
        file_descriptor.write("[var_change] " + "i =" + str(i) + "\n")

        j = 0
        file_descriptor.write("[var_change] " + "j =" + str(j) + "\n")

        k = 0
        file_descriptor.write("[var_change] " + "k =" + str(k) + "\n")

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                a[k] = left_half[i]
                file_descriptor.write("[var_change] " + "a =" + str(a) + "\n")

                i += 1
            else:
                a[k] = right_half[j]
                file_descriptor.write("[var_change] " + "a =" + str(a) + "\n")

                j += 1
            k += 1

        while i < len(left_half):
            a[k] = left_half[i]
            file_descriptor.write("[var_change] " + "a =" + str(a) + "\n")

            i += 1
            k += 1

        while j < len(right_half):
            a[k] = right_half[j]
            file_descriptor.write("[var_change] " + "a =" + str(a) + "\n")

            j += 1
            k += 1
    print("Merging ", a)

merge_sort(a_list)
file_descriptor.close()