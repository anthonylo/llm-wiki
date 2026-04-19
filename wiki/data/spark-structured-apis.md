---
title: Spark Structured APIs (DataFrames, SQL, Datasets)
tags: [spark, dataframe, sql, lazy-evaluation, dag, transformations, actions, structured-streaming]
source: "The-Data-Engineers-Guide-to-Apache-Spark.pdf — The Data Engineer's Guide to Apache Spark (Databricks, 2017)"
---

## Summary

Spark's Structured APIs — DataFrames, Datasets, and SQL Tables — are the recommended high-level interface for most Spark workloads. They all compile to the same underlying execution plan, so there is no performance difference between writing SQL and DataFrame code. The core execution model is **lazy evaluation**: transformations build up a logical plan (DAG) without executing; actions trigger compilation into an optimized physical plan and execute it across the cluster. Narrow transformations pipeline in memory; wide transformations (shuffles) require network data exchange and write to disk. DataFrames are distributed across a cluster, unlike Pandas/R DataFrames which are limited to one machine.

## Explanation

### The Structured API Hierarchy

```
Low-Level APIs
  Distributed variables (broadcast, accumulators)
  RDDs

Structured APIs
  Datasets    DataFrames    SQL Tables

Standard Libraries
  Structured Streaming   MLlib   GraphX   Deep Learning packages
```

**DataFrames**: Most common Structured API. Represents a table with rows and columns. Available in all languages. Schema defines column names and types.

**Datasets**: Type-safe structured API (Scala/Java only). Provides compile-time type checking that DataFrames sacrifice for language flexibility.

**SQL Tables / Views**: `createOrReplaceTempView()` registers any DataFrame as a queryable table. `spark.sql(query)` runs SQL and returns a DataFrame.

All three are backed by the same optimization engine (Catalyst) and produce identical physical execution plans. SQL and DataFrame code for the same logic compile to the same plan:

```
== Physical Plan ==
*HashAggregate(keys=[DEST_COUNTRY_NAME#182], functions=[count(1)])
+- Exchange hashpartitioning(DEST_COUNTRY_NAME#182, 5)
+- *HashAggregate(keys=[DEST_COUNTRY_NAME#182], functions=[partial_count(1)])
+- *FileScan csv [DEST_COUNTRY_NAME#182] ...
```
(Same plan from both SQL `GROUP BY` and DataFrame `.groupBy().count()`)

### Partitions

Partitions are how data is physically distributed across the cluster during execution. A partition is a collection of rows on one physical machine.

- Parallelism = min(number of partitions, number of executors)
- 1 partition → parallelism of 1, even with thousands of executors
- Many partitions + 1 executor → parallelism of 1

With Structured APIs, partitions are managed automatically — users specify high-level transformations; Spark determines physical execution. Default shuffle partitions: 200 (configurable via `spark.conf.set("spark.sql.shuffle.partitions", N)`).

### Transformations

**Transformations are instructions to Spark about how to modify a dataset.** They are **lazy** — they record the transformation in the logical plan without executing it.

| Transformation type | Description | Examples | Execution |
|-------------------|-------------|----------|-----------|
| **Narrow** | Each input partition → at most one output partition | `filter`, `map`, `select`, `withColumn` | Pipelined in memory |
| **Wide (shuffle)** | Input partitions → many output partitions | `groupBy`, `sort`, `join`, `distinct` | Network exchange, written to disk |

Narrow transformations can be pipelined: multiple filters applied to the same partition without intermediate materialization. Wide transformations trigger a **shuffle**: Spark writes intermediate results to disk and redistributes data across the network by partition key.

Shuffle optimization is critical for performance — minimizing wide transformations, using broadcast joins for small tables, and tuning partition counts are key levers.

### Actions

**Actions trigger the actual execution** of the accumulated transformation plan. Three categories:

1. **View data in console**: `show()`, `printSchema()`
2. **Collect data to native objects**: `collect()` (returns array), `take(N)` (returns first N rows), `count()` (returns integer)
3. **Write to output data sources**: `write.format(...).save(path)`

When an action is called, Spark:
1. Compiles the logical transformation DAG into an optimized physical plan
2. Schedules tasks across executors
3. Executes and returns the result

### Lazy Evaluation and DAG Execution

Lazy evaluation means Spark waits until the last moment to execute. Benefits:

**Optimization opportunities**: Spark compiles the entire pipeline from source to action before executing, enabling:
- **Predicate pushdown**: A filter specified late in the plan is pushed down to the data source, minimizing data loaded
- **Column pruning**: Only read columns that are actually used
- **Stage coalescing**: Combine multiple narrow transformations into a single stage

**Execution plan inspection**: `explain()` on any DataFrame shows the logical and physical plan before execution. Physical plans are read top-to-bottom (result to source).

**Example plan for 7-step query** (read → groupBy → sum → rename → sort → limit → collect):
```
TakeOrderedAndProject(limit=5, orderBy=[destination_total DESC], ...)
+- *HashAggregate(keys=[DEST_COUNTRY_NAME], functions=[sum(count)])
+- Exchange hashpartitioning(DEST_COUNTRY_NAME, 5)
+- *HashAggregate(keys=[DEST_COUNTRY_NAME], functions=[partial_sum(count)])
+- InMemoryTableScan...
```

The optimizer merges the two `HashAggregate` steps (partial aggregation at each node, then final aggregation) and produces a `TakeOrderedAndProject` that combines sort + limit.

### SparkSession

The entry point to Spark. One SparkSession per Spark application. Manages the Spark application state and is the interface for executing user-defined transformations.

In interactive mode (`spark-shell` for Scala, `pyspark` for Python): SparkSession is created implicitly and available as `spark`.

In production applications (submitted via `spark-submit`): SparkSession must be created explicitly.

### DataFrames vs RDDs

The 2010 Spark paper (see [[apache-spark]]) introduced RDDs as the primary interface. The Structured API (introduced in Spark 1.3, matured in Spark 2.x) supersedes RDDs for most use cases:

| Property | RDD | DataFrame |
|---------|-----|-----------|
| Interface level | Low-level | High-level |
| Type safety | JVM typed | Schema-typed |
| Optimization | Manual | Catalyst optimizer |
| Performance | Depends on user code | Consistently optimized |
| Language support | Scala, Java, Python, R | All languages + SQL |
| Use case | Custom transformations, streaming | Analytics, ETL, ML |

**Key difference**: RDD operations are **untyped** (arbitrary Scala/Java objects) and **un-optimized** (Spark executes exactly what you write). DataFrame operations go through the Catalyst optimizer which can reorder, merge, and push down operations for better performance.

When to use RDDs: operations that require precise control over physical execution, custom serialization formats, or using Spark's lower-level APIs for streaming and graph processing.

### Structured Streaming

Spark's Structured Streaming treats **live data streams as unbounded tables** — new data is appended as new rows, and queries run continuously as new data arrives. The same DataFrame/SQL API applies; Spark handles the continuous execution, state management, and exactly-once semantics.

### Machine Learning and Advanced Analytics

Spark MLlib provides distributed implementations of common ML algorithms (classification, regression, clustering, collaborative filtering) that operate on DataFrames. Key advantage: the same cluster that processes ETL pipelines can run ML training, without moving data to a separate system.

## Related Pages

- [[apache-spark]] — Spark architecture, MapReduce motivation, RDDs, performance benchmarks
- [[resilient-distributed-datasets]] — The lower-level abstraction that DataFrames are built on
- [[vector-databases-and-embeddings]] — Vector databases handle similarity search at scale; Spark DataFrames handle structured analytics at scale — complementary in ML pipelines

## Contradictions

> **SQL and DataFrame performance equivalence**: The guide states "there is no performance difference between writing SQL queries or writing DataFrame code." This is true after the Catalyst optimizer processes both into the same physical plan. However, complex user-defined functions (UDFs) in Python/R bypass the optimizer and execute as unoptimized row-by-row operations — potentially orders of magnitude slower. The equivalence claim holds for the standard Spark built-in functions and SQL, but breaks for custom UDFs, especially in non-JVM languages.

> **200 default shuffle partitions**: Spark defaults to 200 partitions for shuffles (`spark.sql.shuffle.partitions=200`). The guide notes this should be tuned — for small datasets, 200 partitions creates significant overhead; for very large datasets, 200 may be far too few. There is no universally correct default. The guide implies users should set this to 5 for the example workload; production users must tune based on data size, cluster size, and query characteristics. The default of 200 is widely acknowledged as a frequent source of performance problems for both small and large datasets.

> **DataFrames "always available" vs RDD precedence**: The guide introduces DataFrames as the primary abstraction ("The DataFrame is the most common Structured API"). The original Spark paper (2010) makes no mention of DataFrames — they didn't exist until Spark 1.3 (2015). The field's narrative has shifted: practitioners now learn DataFrames first and encounter RDDs only when they need low-level control. This represents a successful API migration, but creates a risk where practitioners using the Structured API don't understand the underlying execution model (shuffles, lineage, partitions) that determines their code's performance.
