# Luminous-proof-of-concept
#### [Investigation phase]

Proof of concept for the algorithm's interpreter and visualiser

### Idea

Learning is the process which every software engineer should be familiar with. Unfortunately there are a lot of difficulties that prevent from effective learning. There is a common principle which declares that complexity depends on the number of components of a problem you don't know. It's like an equation with multiple variables, existence of each variable increases the complexity of the solution. It could be applied to many areas of people's activity. So the key point in this is next: ***reduce number of unknown to reduce complexity.***

### Goal

*To reduce complexity of the learning algrorithms.*

The way of solving this problem is in presentation of the ideas that lay inside algorithms.
One of the approaches is to show what algorithm actually does (instead of how it's actually implemented). In this case we interact with common concept (no math analysis, no difficulties with specific programming language).

***The main goal is to create effective way to present algorithms.***

At this moment (2016) there are no widely used best practices for such kind of task. In 70th there were flowcharts, unfortunately they have no a lot of effort. 

### Input

- **\*.py** - source file with implemented algorithm in Python.


### Output

- **transformed_source_code.out**: transformed source code(received as input) with additional file write calls.
- **data_collection.out**: data gathered during the evalution of the *transformed_source_code.out* source file

### Usage

##### Common

Run from command-line interface:

`./luminous.py --source-file SOURCE_FILENAME`

where SOURCE_FILENAME - file with algorithm implemented using Python 2.7

##### Examples

There are some examples lay out in the **./samples/** folder. Try them out using next command:

`./luminous.py --source-file ./samples/merge_sort.py`

##### Troubleshooting

Make sure that `luminous.py` file has permissions to execute, otherwise use following command:

`chmod +x luminous.py`

### Limitations

There is a couple of items to simplify scope of work at early stages:

1) Algorithms should mostly be described as set of changes on the input data to produce output data. Ideal examples for such definition will be next types: sort, search. 

(In opposite there are drawing algorithms and other type of algorithms which does not produce explicit output).

2) Limited support of the data structures (user defined classes). TBD
