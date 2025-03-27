
def heuristic(input_data):
    """Minimize makespan with SPT and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                min_time = min(times)
                eligible_operations.append((job, op_num, machines, times, min_time))

        # SPT (Shortest Processing Time) rule
        eligible_operations.sort(key=lambda x: x[4])

        job, op_num, machines, times, _ = eligible_operations[0]

        # Assign to the least loaded machine
        best_machine = min(machines, key=lambda m: machine_available_time[m])
        machine_idx = machines.index(best_machine)
        processing_time = times[machine_idx]
        start_time = max(machine_available_time[best_machine], job_completion_time[job])

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = start_time + processing_time
        job_completion_time[job] = start_time + processing_time
        remaining_operations[job].pop(0)

    return schedule
