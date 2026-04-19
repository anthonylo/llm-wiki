---
title: MapReduce
tags: [mapreduce, distributed-computing, google, programming-model, dean, ghemawat]
source: "mapreduce-osdi04.pdf — MapReduce: Simplified Data Processing on Large Clusters (Dean & Ghemawat, Google, OSDI 2004)"
---

## Summary

MapReduce is a programming model and runtime system for processing large datasets on clusters of commodity machines (Dean & Ghemawat, 2004). Users express computation as two functions — **Map** and **Reduce** — and the runtime handles parallelization, data distribution, fault tolerance, and load balancing automatically. By the time of publication, hundreds of MapReduce programs had been implemented at Google and over 1,000 jobs ran on Google's clusters every day.

## Explanation

### The Programming Model

The computation takes a set of input key/value pairs and produces a set of output key/value pairs. Users supply two functions:

```
map    (k1, v1)       → list(k2, v2)
reduce (k2, list(v2)) → list(v2)
```

**Map**: applied to each input record; emits zero or more intermediate key/value pairs.

**Reduce**: receives an intermediate key and all values associated with that key; merges them into a smaller set of values (typically zero or one output value per invocation).

The MapReduce library groups all intermediate values with the same key and passes them together to the Reduce function. An iterator is used so lists too large to fit in memory can still be processed.

### Type System

Conceptually typed, even though the Google C++ implementation passes raw strings:

```
map    (k1, v1)       → list(k2, v2)
reduce (k2, list(v2)) → list(v2)
```

Input keys/values are from a different domain than output keys/values; intermediate keys/values are from the same domain as the output.

### Canonical Example: Word Count

```cpp
// Map: emit (word, "1") for each word in a document
map(String key, String value):
    for each word w in value:
        EmitIntermediate(w, "1");

// Reduce: sum all counts for a given word
reduce(String key, Iterator values):
    int result = 0;
    for each v in values:
        result += ParseInt(v);
    Emit(AsString(result));
```

### Applications at Google

The model is broad enough to express many real-world computations:

| Application | Map | Reduce |
|------------|-----|--------|
| Distributed Grep | emit line if matches pattern | identity (pass through) |
| URL Access Frequency | emit (URL, 1) per log entry | sum all values for same URL |
| Reverse Web-Link Graph | emit (target, source) per link | concatenate all sources per target |
| Term Vector per Host | emit (hostname, term-vector) per doc | merge term vectors, drop infrequent terms |
| Inverted Index | emit (word, doc-id) per word | sort doc-ids, emit (word, list(doc-id)) |
| Distributed Sort | emit (key, record) | identity (ordering guaranteed by framework) |

### Scale at Google (August 2004)

| Metric | Value |
|--------|-------|
| Jobs run in August 2004 | 29,423 |
| Average job completion time | 634 seconds |
| Machine-days used | 79,186 |
| Input data read | 3,288 TB |
| Intermediate data produced | 758 TB |
| Output data written | 193 TB |
| Average worker machines per job | 157 |
| Average worker deaths per job | 1.2 |

### Large-Scale Indexing (Google Web Search)

The most significant early use: a complete rewrite of Google's production web search indexing system as a sequence of 5–10 MapReduce operations over >20 TB of raw document data. Benefits included:

- Code size reduction: one phase went from ~3,800 lines of C++ to ~700 lines
- Conceptually unrelated computations could be kept separate (no mixing for efficiency reasons)
- Machine failures, slow machines, and network hiccups handled automatically

## Related Pages

- [[mapreduce-execution]] — 7-step execution flow, master/worker architecture, task granularity
- [[mapreduce-fault-tolerance]] — worker/master failure, re-execution semantics, atomic commits
- [[mapreduce-optimizations]] — data locality, backup tasks, combiner function
- [[apache-spark]] — Spark was designed explicitly to address MapReduce's limitations for iterative workloads
- [[resilient-distributed-datasets]] — RDDs provide in-memory fault tolerance that MapReduce's disk-based model lacks

## Contradictions

> **MapReduce vs Spark on iterative workloads**: [[apache-spark]] characterizes MapReduce as unsuitable for iterative ML because every stage reads from and writes to disk. The MapReduce paper doesn't discuss iterative algorithms and presents disk writes of intermediate data as a feature (enabling re-execution for fault tolerance), not a limitation. The limitation only became apparent as ML workloads emerged. The paper's claim that the model is broadly applicable is true for its target workloads (batch ETL, indexing, sorting) but not for iterative graph or ML algorithms.

> **Single master as SPOF**: The paper acknowledges that master failure causes the entire job to abort — clients must retry. This is presented matter-of-factly ("its failure is unlikely"). [[resilient-distributed-datasets]] eliminates this concern at the data layer through lineage, but Spark still has a driver process with similar SPOF characteristics. The problem migrated upward, not away.
