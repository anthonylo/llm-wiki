---
title: Apache Spark
tags: [spark, distributed-computing, cluster-computing, rdd, mapreduce, zaharia, databricks, big-data]
source: "Spark-Cluster-Computing-with-Working-Sets.pdf — Spark: Cluster Computing with Working Sets (Zaharia et al., 2010); The-Data-Engineers-Guide-to-Apache-Spark.pdf — The Data Engineer's Guide to Apache Spark (Databricks, 2017)"
---

## Summary

Apache Spark (Zaharia et al., 2010, UC Berkeley) is a cluster computing framework designed for applications that **reuse a working set of data across multiple parallel operations**. MapReduce and its variants process data through acyclic data flows that require reloading from disk on each pass — an expensive operation for iterative ML algorithms and interactive analytics. Spark introduces **Resilient Distributed Datasets (RDDs)**: read-only, partitioned collections that can be explicitly cached in memory and rebuilt via lineage if lost. Spark can outperform Hadoop by 10× on iterative machine learning workloads and supports interactive querying of a 39 GB dataset with sub-second response time (vs. tens-of-seconds latency for Hadoop).

## Explanation

### Why MapReduce Falls Short

MapReduce built its scalability and fault tolerance on an **acyclic data flow model**: input data passes through a fixed map → reduce graph, results are written to distributed storage, and no state persists between jobs.

Two common workload classes break this assumption:

**1. Iterative jobs** — Machine learning algorithms (gradient descent, logistic regression, ALS) apply a function repeatedly to the same dataset. Each iteration as a MapReduce job reloads the full dataset from disk, even though the data is unchanged. For logistic regression on a 29 GB dataset on 20 EC2 nodes: Hadoop takes **127 seconds per iteration**; Spark takes **174 seconds for the first iteration** (loading + Scala overhead) then **6 seconds for subsequent iterations** (cached data) — up to **10× faster**.

**2. Interactive analysis** — Ad-hoc queries with Pig/Hive run as separate MapReduce jobs, each with tens of seconds of startup latency. A user who wants to explore a dataset iteratively cannot work in a responsive feedback loop.

### Core Architecture

A Spark application consists of:

**Driver process**: Runs the user's `main()` function on a node in the cluster. Responsible for maintaining application state, responding to user input, and analyzing/distributing/scheduling work across executors. One driver per application.

**Executor processes**: Execute code assigned by the driver; report computation state back to the driver. Multiple executors per cluster, configurable per node.

**Cluster manager**: Controls physical machines and allocates resources. Options: Spark Standalone, YARN, Mesos. Multiple Spark applications can share a cluster simultaneously. The original implementation ran on **Mesos** ("cluster operating system" allowing fine-grained sharing).

**SparkSession**: The user-facing entry point — one SparkSession per Spark application. The driver process manifests to the user as a SparkSession object.

**Local mode**: Driver and executors run as threads on a single machine — no cluster required. Useful for development.

### Resilient Distributed Datasets (RDDs)

The core abstraction. See [[resilient-distributed-datasets]] for full detail.

An RDD is a **read-only collection of objects partitioned across a set of machines** that can be rebuilt if a partition is lost. Key properties:

- **Lazy and ephemeral by default**: partitions are materialized on demand and discarded after use
- **Cacheable**: `cache()` keeps the dataset in memory across operations
- **Fault-tolerant via lineage**: the RDD object carries enough information to recompute any partition from data in reliable storage — only lost partitions are recomputed, in parallel, not the entire dataset

Four ways to construct an RDD:
1. From a file in a shared filesystem (HDFS)
2. By "parallelizing" a Scala collection (split into slices sent to multiple nodes)
3. By transforming an existing RDD (`flatMap`, `map`, `filter`)
4. By changing the persistence of an existing RDD (`cache()`, `save()`)

### Structured APIs: DataFrames, SQL, Datasets

The original 2010 paper focused on RDDs. By 2017 (The Data Engineer's Guide), Spark had added **Structured APIs** that are higher-level, more optimized, and the recommended interface for most workloads. See [[spark-structured-apis]].

**DataFrame**: The most common Structured API. Represents a table of data with rows and columns (a schema). A Spark DataFrame is distributed across a cluster, unlike Pandas or R DataFrames which are limited to one machine. DataFrames, SQL Tables, and Datasets compile to the same underlying execution plan — there is no performance difference between writing SQL and DataFrame code.

**Transformations vs Actions**:
- **Transformation**: An instruction to modify a DataFrame/RDD. Returns a new DataFrame. Does NOT execute immediately. Examples: `filter`, `map`, `groupBy`, `sort`, `join`
- **Action**: Triggers the execution of the accumulated transformation plan. Returns a result to the driver or writes to storage. Examples: `count`, `collect`, `take`, `write`

**Lazy evaluation**: Spark builds a DAG (Directed Acyclic Graph) of transformations and compiles it into an optimized physical plan before executing. This enables optimizations like **predicate pushdown** (pushing filters to data sources to minimize data loaded).

**Narrow vs Wide transformations**:
- **Narrow**: Each input partition contributes to at most one output partition. Pipelined in memory (e.g., `filter`, `map`)
- **Wide (shuffle)**: Input partitions contribute to multiple output partitions. Requires exchanging data across the network and writing to disk (e.g., `groupBy`, `sort`, `join`)

### Shared Variables

Beyond RDDs, Spark provides two restricted types of shared variables:

**Broadcast variables**: A read-only value (e.g., a lookup table) distributed to all workers once, rather than packaged with every closure. Without broadcast, a shared dataset is re-sent to each node on every iteration — for ALS matrix factorization, using broadcast variables improved performance by **2.8× on a 30-node cluster**.

**Accumulators**: Variables that workers can only add to (using an associative operation) and that only the driver can read. Used for implementing counters. Fault-tolerant because Spark applies updates from each partition of each operation only once (prevents double-counting on task re-execution).

### Performance Results (Original Paper, 2010)

| Workload | Hadoop | Spark | Speedup |
|---------|--------|-------|---------|
| Logistic regression (subsequent iters, 29 GB, 20 nodes) | 127s/iter | 6s/iter | **21×** |
| Interactive 39 GB Wikipedia query (subsequent queries) | ~35s | 0.5–1s | **35–70×** |
| ALS with broadcast variables vs naïve | — | 2.8× over no-broadcast | — |

**Fault tolerance overhead**: In the 10-iteration logistic regression case, crashing a node slowed the job by 50s (21%) on average. Lost partitions are recomputed in parallel on other nodes.

### Language APIs

Spark is primarily written in Scala (default), with full APIs in Java, Python, R, and SQL. When using Structured APIs, all languages produce the same underlying execution plan and have equivalent performance characteristics. Python/R users never write explicit JVM instructions — Spark translates Python/R code to JVM execution on workers.

## Related Pages

- [[resilient-distributed-datasets]] — RDD properties, lineage, caching, shared variables in detail
- [[spark-structured-apis]] — DataFrames, SQL, transformations vs actions, lazy evaluation, DAG execution
- [[agentic-skills]] — Agentic skills solve the same "reuse across operations" problem for LLM agents that Spark solved for data processing; procedural memory for agents vs working set memory for data

## Contradictions

> **RDDs vs DataFrames as the primary abstraction**: The 2010 Spark paper presents RDDs as the fundamental contribution. The 2017 Data Engineer's Guide presents DataFrames as "the most common Structured API" and "the easiest and most efficient," with RDDs covered in "Part III" as a lower-level fallback. The field has largely moved from RDD-level programming to DataFrame/SQL-level programming — the optimizer (Catalyst) and memory management (Tungsten) for Structured APIs achieve better performance than hand-tuned RDD code in most cases. The original paper's primary contribution (RDDs) has been partially superseded by the higher-level APIs it enabled.

> **Fault tolerance: lineage vs checkpointing**: The original paper argues lineage is superior to checkpointing because only lost partitions need to be recomputed in parallel, rather than reverting to a full checkpoint. However, lineage-based recovery is expensive for long lineage chains — if a partition at the end of a 100-step chain is lost, all 100 steps must be recomputed. Spark later added optional checkpointing to truncate lineage for long-running iterative jobs, acknowledging that pure lineage has practical limits.

> **Local aggregation vs distributed reduction**: The 2010 paper notes "Spark does not currently support a grouped reduce operation as in MapReduce; reduce results are only collected at one process." This was a significant limitation compared to Hadoop's map-side partial aggregation, which reduces shuffle volume. Spark later added `groupBy` + `agg` and shuffle-based reductions in the Structured API — but the 2010 paper's claim that single-reducer suffices to express "a variety of useful algorithms" understates the performance impact of missing map-side combiners.
