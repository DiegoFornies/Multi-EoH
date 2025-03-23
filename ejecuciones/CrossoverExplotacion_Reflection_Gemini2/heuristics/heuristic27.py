
def heuristic(input_data):
    """A heuristic for FJSSP focusing on minimizing idle time and balancing machine load.
    Prioritizes operations with fewer machine options and shorter processing times."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op in enumerate(job_ops):
            operations.append((job_id, op_idx, op))

    # Sort operations based on number of possible machines and processing time
    operations.sort(key=lambda x: (len(x[2][0]), min(x[2][1])))

    for job_id, op_idx, op in operations:
        machines, times = op

        # Find the best machine based on earliest available time
        best_machine, min_end_time = None, float('inf')
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_time = times[i]

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
    
    return schedule
