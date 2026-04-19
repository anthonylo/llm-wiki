---
title: MapReduce Optimizations
tags: [mapreduce, distributed-computing, locality, backup-tasks, stragglers, combiner, partitioning]
source: "mapreduce-osdi04.pdf — MapReduce: Simplified Data Processing on Large Clusters (Dean & Ghemawat, Google, OSDI 2004)"
---

## Summary

The MapReduce runtime includes four key optimizations beyond the basic model: data locality scheduling (co-locating computation with input data to avoid network transfers), backup tasks (redundant execution of near-complete tasks to eliminate straggler bottlenecks), the combiner function (partial pre-aggregation on map workers before network shuffle), and custom partitioning functions (user-controlled assignment of keys to reduce partitions). Together these reduce wall-clock time significantly — backup tasks alone reduce sort job completion time by 44%.

## Explanation

### Data Locality

**Problem**: network bandwidth is scarce. Transferring terabytes of input data from storage to compute nodes saturates the network.

**Solution**: the master knows where GFS has placed replicas of each input file block (GFS stores 3 copies per 64 MB block). When scheduling a map task, the master:

1. Tries to schedule the map task on a machine that *holds a replica* of the input data
2. Failing that, schedules it *near* a replica (e.g., on the same network switch)

**Result**: in large MapReduce operations, "most input data is read locally and consumes no network bandwidth." The sort benchmark shows input rate (13 GB/s) higher than shuffle rate, confirming most input was read from local disks.

This optimization is only possible because MapReduce uses a restricted programming model — pure functions with no side effects — which allows the runtime to freely choose where to execute each task.

### Backup Tasks (Straggler Mitigation)

**Problem**: stragglers — machines that take unusually long to complete their last few tasks — determine the total job duration. Causes include bad disks (30 MB/s → 1 MB/s), competing processes consuming CPU/memory/disk/network, and hardware bugs (e.g., disabled processor caches caused 100× slowdown).

**Solution**: when a MapReduce operation is *close to completion*, the master schedules **backup executions** of all remaining in-progress tasks. The task is marked complete when *either* the primary or the backup execution finishes.

**Cost**: increases total computational resources used by "no more than a few percent."

**Measured impact** (sort benchmark, 1 TB, 1,800 machines):
- Normal execution: **891 seconds**
- Backup tasks disabled: **1,283 seconds** (+44%)
- 200/1,746 workers intentionally killed mid-job: **933 seconds** (+5% vs normal — backup tasks absorbed the failures)

### Combiner Function

**Problem**: some reduce operations (commutative and associative ones, like word count) produce massive repetition in intermediate keys. Word count emits `(the, 1)` thousands of times per map task; all of these are sent over the network to one reduce worker, which sums them.

**Solution**: an optional **Combiner function** runs on each map worker *before* the intermediate data is sent over the network. It performs partial aggregation locally.

- Same code as the Reduce function (the library handles the difference)
- Output of Combiner → intermediate file (sent to reduce worker)
- Output of Reduce → final output file
- Multiple partial sums from the same map worker are merged into one before network transfer

**Effect**: "partial combining significantly speeds up certain classes of MapReduce operations." Not quantified in the paper with a specific benchmark, but the word count example shows the mechanism clearly: instead of sending 100,000 `(the, 1)` records, the combiner emits one `(the, 100000)`.

**Restriction**: only valid when the reduce operation is commutative and associative. Cannot be used for operations like median, where partial results cannot be combined correctly.

### Custom Partitioning Functions

**Default**: `hash(key) mod R` — distributes intermediate keys roughly uniformly across R reduce partitions.

**Problem**: uniform distribution is not always desirable. URL-keyed data may benefit from grouping all URLs from the same host into one output file (for subsequent per-host analysis).

**Solution**: users supply a custom partitioning function. Example: `hash(Hostname(url_key)) mod R` groups all URLs from the same host into the same reduce partition and output file.

### Ordering Guarantees

Within each partition, intermediate key/value pairs are processed in *increasing key order*. This is a consequence of the sort step reduce workers apply after reading all intermediate data for their partition. Benefits:

- Output files per partition are sorted by key
- Enables efficient random-access lookups in output files
- Makes downstream sorted-merge operations cheap

## Related Pages

- [[mapreduce]] — Programming model and applications
- [[mapreduce-execution]] — Task granularity, shuffle mechanism, partitioning
- [[mapreduce-fault-tolerance]] — Re-execution semantics that backup tasks depend on
- [[apache-spark]] — Spark's narrow vs wide transformation distinction maps directly onto map-phase vs shuffle-phase; Spark's in-memory caching eliminates the disk write that MapReduce performs between stages
- [[resilient-distributed-datasets]] — Broadcast variables serve a similar role to MapReduce's combiner: reducing data transferred to workers

## Contradictions

> **Backup tasks and non-determinism**: Backup tasks work correctly for deterministic operators — the primary and backup produce identical output, so whichever finishes first wins. For non-deterministic operators, the paper acknowledges weaker semantics (see [[mapreduce-fault-tolerance]]). Backup tasks amplify this: now *three* possible outputs for a given reduce task exist (primary, backup, and any re-executions from failures). The paper asserts this is "still reasonable" but does not define "reasonable" precisely. Systems requiring strict reproducibility cannot use backup tasks with non-deterministic operators.

> **Combiner correctness boundary**: The paper restricts combiners to commutative and associative operations but does not provide a runtime check or type-system enforcement. A user who incorrectly applies a combiner to a non-associative operation (e.g., computing an average by dividing a running sum by a running count) will get silently wrong results. The paper places this responsibility entirely on the programmer with no tooling support.

> **Locality vs backup tasks interaction**: Data locality schedules map tasks on machines holding input replicas. Backup tasks schedule *additional* copies of in-progress tasks on whatever machines are available — which may not have local replicas. A backup map task for a large input split therefore reads its input over the network, partially defeating the locality optimization. The paper does not discuss this interaction or measure its cost. In practice, backup tasks are launched late in the job when most input has already been processed locally, so the impact is small but not zero.
