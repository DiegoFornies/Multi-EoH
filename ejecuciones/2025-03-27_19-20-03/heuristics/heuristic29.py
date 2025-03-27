
def heuristic(input_data):
    """Schedules jobs using a shortest processing time (SPT) and earliest start time heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations to schedule, sorted by shortest processing time first
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            min_time = float('inf')
            best_machine = None
            for i, m in enumerate(machines):
                if times[i] < min_time:
                    min_time = times[i]
                    best_machine = m
            operations.append((job, op_idx + 1, best_machine, min_time, machines, times))
    
    # Sort operations by shortest processing time
    operations.sort(key=lambda x: x[3])

    for job, op_num, best_machine, min_time, machines, times in operations:
        # Find the earliest possible start time for this operation
        start_time = max(machine_available_times[best_machine], job_completion_times[job])
        end_time = start_time + min_time

        # Update the schedule
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': min_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
