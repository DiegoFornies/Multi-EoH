
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine load and operation processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []

    # Create a list of operations with their job and operation index
    operations = []
    for job in jobs:
        for op_idx, (machines, times) in enumerate(jobs[job]):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on shortest processing time.
    operations.sort(key=lambda x: min(x[3]))  # Sort by shortest possible processing time.

    job_completion_times = {job: 0 for job in jobs}

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the machine with the earliest available time, considering job constraints.
        best_machine = None
        min_start_time = float('inf')

        for m_idx, m in enumerate(machines):
            start_time = max(machine_time[m], job_completion_times[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                best_time = times[m_idx]

        start = min_start_time
        end = start + best_time

        schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine, 'Start Time': start, 'End Time': end, 'Processing Time': best_time})

        machine_time[best_machine] = end
        job_completion_times[job] = end
        machine_load[best_machine] += best_time

    return schedule
