import random

def generate_random_list(n, min_value, max_value):
    list = []
    for i in range(1, n):
        generated_value = random.randint(min_value, max_value)
        list.append(generated_value)
    return list