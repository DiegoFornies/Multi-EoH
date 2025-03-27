
def heuristic(input_data):
    """Combines shortest processing time and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}
    
    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Sort by shortest processing time, then earliest machine availability
        eligible_operations.sort(key=lambda x: (min(x[3]), machine_available_times[min(x[2], key=lambda m:machine_available_times[m])]))
        
        job, op_num, machines, times = eligible_operations[0]
        
        # Choose machine with earliest available time
        best_machine = min(machines, key=lambda m: machine_available_times[m])
        machine_idx = machines.index(best_machine)
        processing_time = times[machine_idx]
        start_time = max(machine_available_times[best_machine], job_completion_times[job])
        end_time = start_time + processing_time

        scheduled_operations[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time
        remaining_operations[job].pop(0)

    return scheduled_operations
