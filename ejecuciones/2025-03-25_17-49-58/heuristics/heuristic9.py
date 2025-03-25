
def heuristic(input_data):
    """A heuristic for the FJSSP that prioritizes minimizing idle time on machines."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations and prioritize them
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by shortest processing time and fewest available machines first.
    operations.sort(key=lambda x: (min(x[3]), len(x[2])))

    for job, op_num, machines, times in operations:
        best_machine, best_time, earliest_start = None, float('inf'), float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = processing_time

        start_time = earliest_start
        end_time = start_time + best_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
