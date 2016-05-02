# Luminous-proof-of-concept
Proof of concept for the Luminous algorithm's interpreter and renderer

### Idea

Learning is the process which every software engineer should be familiar with. Unfortunately there are a lot of difficulties that prevent from effective learning. There is a common principle which declares that complexity depends on the number of components of a problem you don't know. It's like an equation with multiple variables, existence of each variable increases the complexity of the solution. It could be applied to many areas of people's activity. So the key point in this is next: ***reduce number of unknown to reduce complexity.***

### Goal

*To reduce complexity of the learning algrorithms.*

The way of solving this problem is in presentation of the ideas that lay inside algorithms.
One of the approaches is to show what algorithm actually does (instead of how it's actually implemented). In this case we interact with common concept (no math analysis, no difficulties with specific programming language).

***The main goal is to build a visualiser for algorithm.***

At this moment (2016) there are no widely used best practices for such kind of task. In 70th there were flowcharts, unfortunately they have no a lot of effort. 


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

### Technical details

##### Several components:
- *Parser.*
- *Interpreter*
- *Visualiser*

##### Source analyzer

- Task 1. Source analyzer could build tree of variable's dependencies of each other.
- Task 2. Recognizing variable's roles in the output result calculation.

##### Data flow.
- Task 1. Data snapshots diff find out for different types of common data types.


