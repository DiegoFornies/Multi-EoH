
def heuristic(input_data):
    """Heuristic for FJSSP: SPT with machine workload consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Ready queue: (job_id, op_index, machines, times)
    ready_queue = []
    for job_id, operations in jobs.items():
        if operations:
            ready_queue.append((job_id, 0, operations[0][0], operations[0][1]))

    while ready_queue:
        # Shortest Processing Time (SPT) with machine workload consideration
        best_op = None
        min_weighted_time = float('inf')

        for job_id, op_index, machines, times in ready_queue:
            for m_idx, machine in enumerate(machines):
                weighted_time = times[m_idx] + machine_load[machine]
                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_op = (job_id, op_index, machine, times[m_idx])

        # Schedule the best operation
        job_id, op_index, machine, processing_time = best_op
        start_time = max(machine_load[machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine_load and job completion time
        machine_load[machine] = end_time
        job_completion_time[job_id] = end_time

        # Remove scheduled op
        ready_queue.remove((job_id, op_index, jobs[job_id][op_index][0], jobs[job_id][op_index][1]))

        # Add next op to ready queue if exists
        next_op_index = op_index + 1
        if next_op_index < len(jobs[job_id]):
            ready_queue.append((job_id, next_op_index, jobs[job_id][next_op_index][0], jobs[job_id][next_op_index][1]))

    return schedule
