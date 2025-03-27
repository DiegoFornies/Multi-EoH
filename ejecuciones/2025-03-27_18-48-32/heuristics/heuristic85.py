
def heuristic(input_data):
    """Schedules jobs by prioritizing shortest processing time operations."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in jobs:
        schedule[job_id] = []

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Prioritize operations with shortest processing time
        eligible_operations.sort(key=lambda x: min(x[3]))

        job, op_num, machines, times = eligible_operations[0]
        #Select machine with the earliest available time
        best_machine = min(machines, key=lambda m: machine_available_time[m])
        processing_time = times[machines.index(best_machine)]
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
