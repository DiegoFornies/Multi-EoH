
def heuristic(input_data):
    """A heuristic for FJSSP: Random machine selection with earliest start time."""
    import random
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            # Randomly choose a machine from feasible ones.
            chosen_machine_idx = random.randint(0, len(machines) - 1)
            machine = machines[chosen_machine_idx]
            processing_time = times[chosen_machine_idx]

            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job] = end_time

    return schedule
