
def heuristic(input_data):
    """A scheduling heuristic minimizing makespan using shortest processing time (SPT) and earliest start time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []

    # Create a list of operations with job and operation indices
    operations = []
    for job in jobs:
        for op_idx in range(len(jobs[job])):
            operations.append((job, op_idx))

    # Sort operations based on shortest processing time
    operations.sort(key=lambda op: min(jobs[op[0]][op[1]][1]))

    for job, op_idx in operations:
        machines, times = jobs[job][op_idx]

        # Choose machine that allows earliest start time
        best_machine = None
        min_start_time = float('inf')
        best_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_time[machine], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_time = times[m_idx]

        start_time = min_start_time
        end_time = start_time + best_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
