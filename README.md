# RPQ_Data

All the data connected to the multiple source regular path querying algorithm evaluation I did before.

---

Results here are mainly based on 4 graphs: `core`, `eclass`, `enzyme`, `go`. Their deeper descrtiption is [here](https://jetbrains-research.github.io/CFPQ_Data/dataset/index.html).
# What it contains
- The evaluation results of running the algorithm. So they can be later used in comparisents.
- Grammars in the form of regular expressions generated in templates for each graph
- Properties derived from the graphs. That is used in query creation, since we wanted to created queries that use most common labels.
- Utilies for generating regular graph queries from templates.



# Repo structure

```
│
├──eval_results - directory for measurements results
├───grammars - generated queries for corresponding graphs
├──graphs 
│   ├──chunks 
│   │   ├───value - dump of used src verts in absolute value
│   │   ├───percent - dump of used src verts in percentage
│   └──config - the most common labels enumerated
└──utils - tools for query generation

```