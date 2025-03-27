
def heuristic(input_data):
    """Aims to minimize makespan with SPT and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}  # Track machine load
    job_completion = {j: 0 for j in range(1, n_jobs + 1)} # Track job completion times

    # Flatten and sort operations by Shortest Processing Time (SPT) globally
    flattened_ops = []
    for job, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            flattened_ops.append((job, op_idx + 1, machines, times))

    # Sort operations globally by shortest processing time considering all machine options
    flattened_ops.sort(key=lambda x: min(x[3])) #x[3] processing times

    for job, op_num, machines, times in flattened_ops:
        # Find best machine for the current operation based on earliest completion time
        best_machine, min_completion_time = None, float('inf')

        for i, m in enumerate(machines):
            start_time = max(machine_load[m], job_completion[job])
            completion_time = start_time + times[i]

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = m
                best_time_idx = i #index of processing time for this machine

        # Schedule the operation on the best machine
        start_time = max(machine_load[best_machine], job_completion[job])
        end_time = start_time + times[best_time_idx]
        processing_time = times[best_time_idx]

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion[job] = end_time

    return schedule
