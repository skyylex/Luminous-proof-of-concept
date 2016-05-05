#!/usr/bin/python

from subprocess import call
import os

try:
    os.remove("executions.arff")
except OSError:
    pass

files = ["./samples/bubble_sort.py", "./samples/quick_sort.py", "./samples/merge_sort.py", "./samples/insertion_sort.py"]
input_sizes = [10, 50, 100]
iterations_count = 10

for source_file in files:
    for size in input_sizes:
        for i in range(0, iterations_count):
            # tuple = (source_file, size)
            call(["./luminous.py", "--source-file", source_file, "--generate-input", "num_list", "--input-size", str(size)])
