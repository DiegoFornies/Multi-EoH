
def heuristic(input_data):
    """A heuristic to solve FJSSP: Schedules operations greedily, 
    prioritizing short operations and machines with low load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in jobs}
    
    # Priority Queue (Operation, Job, Operation Index)
    import heapq
    available_ops = []

    # Initialize available operations (first operation of each job)
    for job_id, operations in jobs.items():
        if operations:
            heapq.heappush(available_ops, (operations[0][1][0], job_id, 0)) # (Duration, Job, Op_idx)

    while available_ops:
        duration, job_id, op_idx = heapq.heappop(available_ops)
        
        machines, times = jobs[job_id][op_idx]
        
        best_machine, best_time, best_start_time = None, float('inf'), float('inf')

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_last_end_time[job_id])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_time = times[m_idx]

        start_time = best_start_time
        end_time = start_time + best_time
        machine_available_time[best_machine] = end_time
        job_last_end_time[job_id] = end_time
        
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Add next operation of this job to available ops if it exists
        if op_idx + 1 < len(jobs[job_id]):
            next_machines, next_times = jobs[job_id][op_idx+1]
            heapq.heappush(available_ops, (next_times[0], job_id, op_idx + 1))

    return schedule
