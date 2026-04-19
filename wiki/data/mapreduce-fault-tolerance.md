---
title: MapReduce Fault Tolerance
tags: [mapreduce, fault-tolerance, distributed-computing, re-execution, atomic-commits, determinism]
source: "mapreduce-osdi04.pdf — MapReduce: Simplified Data Processing on Large Clusters (Dean & Ghemawat, Google, OSDI 2004)"
---

## Summary

MapReduce achieves fault tolerance through re-execution rather than replication or checkpointing. The master pings workers periodically; failed workers' tasks are reset and rescheduled. Atomic commits of map and reduce output ensure exactly-once semantics for deterministic operators. The master is a single point of failure — if it dies, the job aborts and must be retried. A bad-record skipping mechanism handles crashes caused by deterministic bugs in user code.

## Explanation

### Worker Failure

**Detection**: master pings every worker periodically. No response within a timeout → worker marked as failed.

**Recovery**:
- Any map task *in progress* on the failed worker → reset to `idle`, eligible for rescheduling
- Any reduce task *in progress* on the failed worker → reset to `idle`, eligible for rescheduling
- Map tasks *completed* on the failed worker → also reset to `idle` and re-executed

The asymmetry between completed map tasks and completed reduce tasks is fundamental:
- Completed **map** output sits on the failed machine's **local disk** → inaccessible → must re-execute
- Completed **reduce** output was written to **GFS** → globally accessible → no re-execution needed

When a map task is re-executed on a new worker, all in-progress reduce workers are notified. Reduce workers that had not yet read the map task's output switch to reading from the new worker.

**Real example from the paper**: during network maintenance, 80 machines became unreachable for several minutes. The MapReduce master re-executed the work from the unreachable workers and the job completed successfully.

### Master Failure

**Current implementation**: if the master fails, the MapReduce computation is **aborted**. Clients must detect this and retry. Master failure is considered unlikely because there is only one master.

**Checkpointing**: the master writes periodic checkpoints of its data structures. A new master copy can be started from the last checkpoint, but the paper's implementation does not do this automatically.

This is a genuine single point of failure (SPOF). The paper treats it as acceptable because master hardware failure is rare compared to worker failure (where average is 1.2 worker deaths per job).

### Semantics in the Presence of Failures

**Atomic commits** are the mechanism that guarantees correctness:

- Each in-progress task writes output to **private temporary files**
- A **map task** produces R temporary files (one per reduce partition). When complete, it sends the names of these files to the master. If the master already received a completion message for this map task (duplicate), it ignores the new message.
- A **reduce task** produces one temporary file. When complete, it **atomically renames** it to the final output filename. If the same reduce task runs on multiple machines (e.g., due to backup execution), multiple renames run — the underlying filesystem's atomic rename guarantees the final state contains exactly one execution's output.

**For deterministic operators**: the distributed output is identical to what a sequential, non-faulting execution would have produced.

**For non-deterministic operators**: weaker but still reasonable semantics. If execution e(R1) reads output from one execution of map task M, and e(R2) reads output from a different execution of M (due to re-execution), R1 and R2 may each be equivalent to different sequential executions of the non-deterministic program. The paper considers this acceptable.

### Skipping Bad Records

Sometimes user code has deterministic bugs that crash on specific input records. Fixing the bug is not always possible (e.g., the bug is in a third-party library). The bad-record skipping mechanism:

1. Each worker installs a **signal handler** for segmentation violations and bus errors
2. Before invoking each Map or Reduce call, the library stores the input record's **sequence number** in a global variable
3. If the user code signals, the signal handler sends a **UDP packet** with the sequence number to the master ("last gasp" message)
4. If the master sees **more than one failure** on a particular record's sequence number, it marks that record to be **skipped** on the next re-execution of the corresponding task

This allows a job with a small number of problematic records to make forward progress, at the cost of silently dropping those records.

### Counters: Sanity-Check Mechanism

The counter facility provides an indirect consistency check. Users can assert invariants like "number of output pairs == number of input pairs processed." Counter values from individual workers are propagated to the master (piggybacked on ping responses), aggregated, and deduplicated to avoid double-counting from backup tasks or re-executions. The master displays current counter values on its status page.

## Related Pages

- [[mapreduce]] — Programming model overview
- [[mapreduce-execution]] — Execution flow and master data structures
- [[mapreduce-optimizations]] — Backup tasks (straggler mitigation)
- [[resilient-distributed-datasets]] — RDDs use lineage for fault tolerance instead of re-execution from source; avoids re-reading HDFS but requires lineage chains to remain short
- [[apache-spark]] — Spark's driver is also a single point of failure, analogous to MapReduce's master SPOF

## Contradictions

> **"Master failure is unlikely"**: The paper justifies not handling master failure automatically because only one master exists and hardware failure is rare. This reasoning conflates hardware failure with process failure. A master process can crash due to software bugs, OOM, or OS issues at the same rate as any other process. In the average 29,423-job August 2004 workload, even a 0.01% master crash rate implies ~3 aborted jobs per month. The paper's "acceptable" framing depends on the frequency of master crashes being genuinely negligible, which it does not demonstrate. Subsequent distributed systems (Hadoop YARN, Kubernetes) added master HA as a first-class concern.

> **Atomic rename as fault-tolerance mechanism**: The paper relies on the underlying filesystem providing atomic rename for reduce output correctness. This is true for POSIX filesystems and GFS. However, the paper does not discuss what happens if the reduce worker dies *after* writing the temp file but *before* the rename completes, or if GFS itself experiences a failure during the rename. These are acknowledged to be edge cases handled by GFS's own fault tolerance, but the paper layers correctness guarantees on an external system without fully specifying the dependency.

> **Re-execution vs lineage**: Re-execution from source is simple and correct but costly for long pipelines. A job with 10 chained MapReduce stages that fails on stage 9 must re-read and re-process from stage 1 (or rely on intermediate GFS outputs being preserved). [[resilient-distributed-datasets]] (Zaharia 2010) proposed lineage-based recovery specifically to address this cost for iterative algorithms. The MapReduce paper's fault model is efficient for single-stage jobs but scales poorly in recovery cost as pipeline depth increases.
