
def heuristic(input_data):
    """A scheduling heuristic that considers earliest available machine and shortest processing time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []

    # Flatten operations into a list sorted by shortest processing time
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on shortest processing time available.
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        best_machine, best_time = None, float('inf')
        earliest_start = float('inf')
        chosen_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job])

            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = start_time + processing_time
                chosen_processing_time = processing_time

        start_time = earliest_start
        end_time = best_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': chosen_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
