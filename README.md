# Retiming graph algorithms

Implementation of algorithms WD, OPT1, OPT2, CP from [Leierson - Saxe retiming paper](https://cseweb.ucsd.edu/classes/sp17/cse140-a/exam/LeisersonRetiming.pdf)

You can find the slides of this project at this [link](https://docs.google.com/presentation/d/18XoahbEkRsyzuv5lwZE8kydG6DEL4P2di1DwdYzL58g/edit?usp=sharing)
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install requirements.txt
```
## Structure
The project is divided in folder as follows:
- algorithms: containing the implemented algorithms
- retiming: containing the two classes to instantiate Retiming graphs (random and from node, edges, weights and delays lists)
- performance: memory and time benchmarks
- tests: set of functions to check the correctness of the algorithm

Every function can be called through runner.py via terminal

## Usage

runner.py provides a set of terminal arguments to access and showcase all the different functionalities implemented 
```bash
optional arguments:
  -h, --help            show this help message and exit
  --paper_test_opt      Test OPT1 and OPT2 algorithms on paper and slides graph
  --paper_test_cp       Test CP algorithms on paper and slides graph
  --paper_test_delta_array
                        Test delta array computation on paper and slides graph
  --random_test_opt12   Test OPT1 and OPT2 algorithms on a list of random graphs
  --random_opt1         Test OPT1 algorithm on a random graph
  --random_opt2         Test OPT2 algorithm on a random graph
  --random_wd           Test wd algorithm on a random graph
  --time_instantiation  Test time of instantiation on a list of random graphs
  --time_wd             Test time of WD on a list of random graphs
  --time_opt1           Test time of OPT1 on a list of random graphs
  --time_opt2           Test time of OPT2 on a list of random graphs
  --memory_instantiation
                        Test memory of instantiation on a list of random graphs
  --memory_wd           Test memory of WD on a list of random graphs
  --memory_opt1         Test memory of OPT1 on a list of random graphs
  --memory_opt2         Test memory of OPT2 on a list of random graphs
  --plot_performance    Plot performance graph
  --nodes_list NODES_LIST [NODES_LIST ...]
                        List of random graph number of nodes to run tests
  --weights WEIGHTS     Set weights, random or positive
  --cycle_check         Check for positive cycles
  --n_tests N_TESTS     How many tests for random OPT1 and OPT2 algorithms testing
  --n_nodes N_NODES     Number of random nodes for a random graph
  --edge_prob EDGE_PROB
                        Set edge probability for a random graph
  --verbose             Set verbosity to true
  --draw                Draw graphs
```
Here's some examples on how to launch different functions.

To test OPT1 and OPT2 on the paper graphs:
```bash
python3 runner.py --paper_test_opt
```
To test OPT1 on a random graph, for instance
```bash
python3 runner.py --random_opt1
```
You can add verbosity and draw graph, as well as changing the weights from positive to random and deciding the number of nodes on which an algorithm would be run:
```bash
python3 runner.py --random_opt1 --n_nodes 25 --weights random --verbose --draw
```
### Important remark on weights
to have correct results, if the weights are **random**, we need to perform a cycle checking, which is really slow but assure that the program terminates (due to condition W2 on the paper along cycles there must be at least an edge with strictly positive weight), so it should be run over small number of nodes. If we want to increase the number of nodes significantly weights must be set to **positive**, since the cycle check would not be needed (all weights are positive so no need to check whether there might be null cycles). This holds up for every function. Weights are set **positive by default**, if not specified random

Cycle checking can be enabled with --cycle_check also on positive weights, but it is suggested just to understand its correctness since it becomes useless in that case

### Specifying a list of nodes

To check that OPT1 and OPT2 always return the same result, we can run 
```bash
python3 runner.py --random_test_opt12 --nodes_list 10 20 30 --n_tests 5 --edge_probability 0.5
```
We pass to --nodes_list a list of integer (10 20 30), which means that the algorithm will check that the clock periods from opt1 and opt2 are equal, for three different random graph with respectively 10, 20 and 30 node. We can also specify the number of times we want to run this algorithm with --n_tests. In this example, it will run this algorithm 5 times. 

When using test function, we can specify the edge probability with which the edges will be generated. 

### Performances

We can run memory and temporal benchmark for each algorithm and for the graph instantiation. These functions will run a memory benchmarks given a list of node numbers of the random graphs, then results can be plotted in a matplot graph as well (we can still specify the type of weights to also check the differences in terms of performances):
```bash
python3 runner.py --time_opt1 --nodes_list 10 20 30 --weights random --plot_performance
python3 runner.py --memory_opt1 --nodes_list 10 20 30 --weights positive --plot_performance
```
 
