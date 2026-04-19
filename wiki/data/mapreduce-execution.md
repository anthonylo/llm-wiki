---
title: MapReduce Execution Model
tags: [mapreduce, distributed-computing, master-worker, shuffle, execution, partitioning]
source: "mapreduce-osdi04.pdf — MapReduce: Simplified Data Processing on Large Clusters (Dean & Ghemawat, Google, OSDI 2004)"
---

## Summary

The MapReduce runtime splits input into M pieces, assigns map and reduce tasks to workers via a central master process, buffers intermediate output on local disks, shuffles it across the network to reduce workers, and writes final output to a distributed filesystem. The master tracks all task state and intermediate file locations. M and R (number of map and reduce tasks) are chosen to be much larger than the number of workers, enabling fine-grained load balancing and fast failure recovery.

## Explanation

### Execution Steps (7-Step Flow)

```
1. Split input files into M pieces (16–64 MB each)
   Start copies of program on cluster machines

2. Master assigns M map tasks + R reduce tasks to idle workers

3. Map workers read their input split
   Parse key/value pairs → pass to user Map function
   Buffer intermediate pairs in memory

4. Periodically flush buffered pairs to local disk
   Partition into R regions by partitioning function
   Send file locations back to master

5. Reduce workers notified of locations by master
   Read buffered data via RPC from map workers' local disks
   Sort by intermediate key (external sort if needed)

6. For each unique intermediate key:
   Pass key + all values to user Reduce function
   Append output to final output file for this partition

7. Master wakes up user program
   MapReduce call returns
```

Output available in R output files (one per reduce task). Users typically pass these files directly to another MapReduce call rather than concatenating them.

### Master Data Structures

The master is the coordination hub:

- **Task state**: tracks each map and reduce task as `idle`, `in-progress`, or `completed`, along with the identity of the assigned worker machine
- **Intermediate file locations**: for each completed map task, stores the locations and sizes of R intermediate file regions; pushes this information incrementally to in-progress reduce workers

The master is the only way reduce workers learn where to find intermediate data.

### Partitioning and Ordering

**Partitioning function**: determines which reduce task handles a given intermediate key. Default: `hash(key) mod R`. Users can supply custom partitions — e.g., `hash(Hostname(url)) mod R` to group all URLs from the same host into one output file.

**Ordering guarantee**: within each partition, intermediate key/value pairs are processed in *increasing key order*. This makes it easy to generate sorted output files and enables efficient random-access lookups by key.

### Task Granularity

M and R should be much larger than the number of worker machines:

- More tasks → better dynamic load balancing (faster workers process more tasks)
- More tasks → faster failure recovery (many small map tasks can be redistributed across the remaining workers when one fails)

**Practical constraints**: the master must make O(M + R) scheduling decisions and keeps O(M × R) state in memory (approximately 1 byte per map/reduce task pair). Typical values: M = 200,000, R = 5,000, 2,000 worker machines.

**Input split sizing**: 16–64 MB per piece — tuned to match GFS block size (64 MB) so the locality optimization (scheduling map tasks near their input) is most effective.

**R constraint**: R is often constrained by user requirements because each reduce task produces one output file. Common practice: make R a small multiple of the number of expected worker machines.

### Cluster Environment (Google, 2004)

- Dual-processor x86 machines running Linux, 2–4 GB RAM each
- 100 Mb/s or 1 Gb/s Ethernet per machine (considerably less aggregate bisection bandwidth)
- Hundreds to thousands of machines per cluster; machine failures are common
- Storage: inexpensive IDE disks, managed by GFS (3-way replication)
- Jobs submitted to a scheduling system that maps tasks to available machines

### Performance Benchmarks

**Grep** (1 TB input, pattern in 92,337/10^10 records):
- Peak throughput: >30 GB/s with 1,764 workers
- Total time: ~150 seconds (including ~60 seconds of startup)

**Sort** (1 TB, TeraSort benchmark):
- Peak input rate: ~13 GB/s
- Total time: 891 seconds on 1,700 machines
- Previous best reported: 1,057 seconds
- Backup tasks disabled: 1,283 seconds (+44%)
- 200/1,746 workers intentionally killed mid-job: 933 seconds (+5% vs normal)

## Related Pages

- [[mapreduce]] — Programming model, Map/Reduce functions, applications
- [[mapreduce-fault-tolerance]] — What happens when workers or the master fail
- [[mapreduce-optimizations]] — Locality scheduling, backup tasks, combiner function
- [[resilient-distributed-datasets]] — RDDs replace disk-based intermediate storage with in-memory lineage
- [[spark-structured-apis]] — Narrow vs wide transformations map directly onto MapReduce's map and shuffle phases

## Contradictions

> **Intermediate data locality**: The paper says map workers write intermediate output to *local disk* (not GFS), and reduce workers read it via RPC. This is a deliberate design choice — writing to local disk saves network bandwidth at write time. But it means completed map tasks must be *re-executed* if that machine fails before reduce workers read its output (unlike completed reduce tasks, whose output is in GFS). This asymmetry is presented as a reasonable trade-off but creates a hidden dependency: reduce tasks cannot complete until all map tasks have completed AND their intermediate files are accessible. Long-running reduce tasks that encounter late map task failures must wait for re-execution. The paper does not quantify the frequency of this scenario.

> **R = 5,000 with 2,000 workers**: Each worker may process multiple reduce tasks sequentially. With R >> workers, each worker handles R/workers ≈ 2.5 reduce tasks on average. The paper presents this as good for load balancing, but it also means 5,000 output files per job. Users who want a single sorted output must concatenate 5,000 files or accept one more MapReduce pass. The paper treats this as a non-issue ("users often pass these files as input to another MapReduce call") but it is a real operational complexity.
