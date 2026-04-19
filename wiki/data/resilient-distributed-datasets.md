---
title: Resilient Distributed Datasets (RDDs)
tags: [spark, rdd, fault-tolerance, lineage, distributed-computing, caching, zaharia]
source: "Spark-Cluster-Computing-with-Working-Sets.pdf — Spark: Cluster Computing with Working Sets (Zaharia et al., 2010)"
---

## Summary

Resilient Distributed Datasets (RDDs) are the core abstraction introduced by Spark (Zaharia et al., 2010). An RDD is a **read-only collection of objects partitioned across a set of machines** that can be rebuilt if a partition is lost. RDDs achieve fault tolerance through **lineage**: each RDD object carries enough information about how it was derived from other RDDs to recompute only lost partitions, in parallel, without reverting to a full checkpoint. RDDs represent a sweet spot between expressivity and reliability — restricted enough for efficient fault tolerance, general enough to express iterative ML, interactive analytics, and graph algorithms that acyclic data flow models cannot handle efficiently.

## Explanation

### Formal Properties

An RDD object implements three core operations:

1. **`getPartitions()`** — Returns a list of partition IDs
2. **`getIterator(partition)`** — Iterates over a partition's elements
3. **`getPreferredLocations(partition)`** — Returns preferred locations for task scheduling (data locality)

Different RDD types implement this interface differently:
- `HdfsTextFile`: partitions are HDFS block IDs; preferred locations are block locations; `getIterator` opens a stream to read a block
- `MappedDataset`: partitions and locations same as parent; iterator applies the map function to parent elements
- `CachedDataset`: `getIterator` first checks for a locally cached copy; preferred locations are updated to the caching node after the first computation

### Persistence Model

By default, RDDs are **lazy and ephemeral**: partitions are materialized on demand and discarded from memory after use.

Two actions change persistence:
- **`cache()`**: Leaves the dataset lazy, but hints that it should be kept in memory after the first computation. Subsequent operations reuse cached partitions without recomputation.
- **`save()`**: Evaluates the dataset and writes it to a distributed filesystem (HDFS). The saved version is used in future operations.

**Cache semantics**: Caching is only a hint. If there is not enough memory in the cluster to cache all partitions, Spark will recompute them when needed — analogous to virtual memory. Programs keep working at reduced performance rather than failing.

**Persistence planning**: Future work in the original paper outlined a trade-off framework between: cost of storing the RDD in memory, speed of accessing it, probability of losing part of it, and cost of recomputing it. This was eventually formalized in Spark's memory management system.

### Lineage-Based Fault Tolerance

The key design choice distinguishing RDDs from Distributed Shared Memory (DSM) systems:

**Traditional DSM**: Fault tolerance via checkpointing — the program reverts to the last checkpoint when a node fails, losing all work since. Checkpoint overhead exists even when no nodes fail.

**RDD lineage**: Each RDD object captures its derivation from parent RDDs as a chain of transformations (see Figure 1 in the original paper). If a partition is lost, Spark reconstructs it by replaying the lineage transformations on the original source data. Only the lost partition is recomputed, not the entire dataset. Recovery happens in parallel across multiple nodes.

**Trade-off**: Lineage works well for short lineage chains. For long iterative processes (100+ iterations), lineage chains become expensive to recompute. Spark later introduced optional checkpointing to truncate lineage for long-running jobs — acknowledging that pure lineage has practical limits.

### Comparison to Distributed Shared Memory

| Property | RDD | DSM |
|---------|-----|-----|
| Reads | Coarse-grained (partition-level) | Fine-grained (arbitrary memory addresses) |
| Writes | Coarse-grained (immutable transform) | Fine-grained |
| Fault tolerance | Lineage: recompute lost partitions | Checkpointing or replication |
| Recovery | Parallel, only lost partitions | Full checkpoint restore |
| Stragglers | Mitigated by backup tasks | Difficult |
| Data locality | Push computation to data | Data accessed globally |
| Programming model | Restricted functional | General |

RDDs trade generality (no arbitrary fine-grained writes) for automatic fault tolerance and efficient parallel recovery.

### Parallel Operations on RDDs

Three primary parallel operations:

- **`reduce`**: Combines elements using an associative function, producing a result at the driver program (local reduction performed at each node first)
- **`collect`**: Sends all elements to the driver program
- **`foreach`**: Passes each element through a user-provided function (for side effects — writing to another system or updating a shared variable)

Note: The 2010 paper explicitly states Spark **does not yet support grouped reduce** (map-side combiners as in MapReduce) — `reduce` results are only collected at one process. GroupBy and shuffle-based aggregations were added later in the Structured API.

### Shared Variables

Beyond RDDs, Spark provides two types of shared variables for common patterns that require data to be shared across workers without passing it through every closure:

**Broadcast Variables**

A read-only value distributed to each worker node **once**, cached locally, and reused across parallel operations. Without broadcast, a large lookup table (e.g., the ratings matrix R in ALS) would be re-serialized and sent to each node on every task invocation.

Implementation: The value is saved to a file in a shared filesystem. The serialized form of the broadcast variable is a path to this file. Workers check a local cache before reading from the filesystem.

Performance evidence: ALS collaborative filtering — using broadcast variables for the ratings matrix R improved performance by **2.8×** compared to naïve re-sending on a 30-node EC2 cluster.

**Accumulators**

Variables that workers can only **add to** (using an associative operation) and that only the driver can **read**. Implement counters analogous to MapReduce's built-in counter mechanism.

Fault-tolerant implementation: Each accumulator gets a unique ID at creation. Workers maintain a thread-local copy per task, reset to zero at task start. After each task, the worker sends updates to the driver. The driver applies updates from each partition of each operation **only once** — preventing double-counting when tasks are re-executed due to failures.

Accumulators can be defined for any type with an "add" operation and a "zero" value.

### Scala Implementation Details

Spark integrates into Scala (a statically typed high-level language for the JVM) and exposes a functional programming interface.

**Closures as computation units**: Spark ships tasks to workers by serializing Scala closures as Java objects using Java serialization. This enables the programming model where computation is expressed as functions passed to `map`, `filter`, `reduce` etc.

**Closure serialization bug**: The Scala closure implementation includes references to variables in the closure's outer scope that are not actually used in the body. Spark implements a static analysis of closure classes' bytecode to detect unused variables and null them out before serialization — preventing unintended large object graphs from being shipped to workers.

**Interactive interpreter integration**: Two modifications to the Scala interpreter enable interactive use:
1. Classes defined by the interpreter are output to a shared filesystem so workers can load them
2. Generated code is modified so each line's singleton object references previous lines' singleton objects directly (rather than through static `getInstance` methods) — enabling closures to capture current singleton state when serialized to workers

## Related Pages

- [[apache-spark]] — Overview of Spark, MapReduce limitations, performance benchmarks
- [[spark-structured-apis]] — DataFrames, SQL, transformations/actions built on top of RDDs
- [[agentic-skills]] — Skills are to LLM procedural memory what RDDs are to distributed data processing: a persistent, fault-tolerant working set that survives across operations

## Contradictions

> **Lineage purity vs checkpointing pragmatism**: The original paper presents lineage as strictly superior to checkpointing — no overhead on success, parallel recovery on failure. This is true for short lineage chains. For iterative jobs with many steps (e.g., gradient descent for 1000 iterations), the lineage chain to any partition grows proportionally — recovery requires replaying all 1000 iterations. Spark later added optional `checkpoint()` calls to truncate lineage, writing the RDD to stable storage to create a new root. The 2010 paper's claim that "lineage information is inexpensive to capture" is true; the claim that it's always sufficient for recovery is not.

> **RDD generality vs the options framework comparison**: The paper frames RDDs as related to Sutton et al.'s options framework in RL (temporally extended actions). The analogy is loose: options are policies with initiation sets and termination conditions (a match with [[agentic-skills]]); RDDs are data containers with lineage. The deeper connection is that both frameworks solve the same meta-problem — packaging reusable procedural or data units with enough information to reconstruct their state — but for entirely different domains.

> **Caching as hint vs guarantee**: The paper states caching is "only a hint" and that Spark recomputes partitions if memory is insufficient. This design simplifies the programming model (no explicit memory management) but creates non-deterministic performance: the same program may run 6s/iter with cached data or 127s/iter without. In production, understanding when Spark evicts cached partitions requires examining memory management internals that the simple "hint" abstraction deliberately hides.
