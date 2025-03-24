
def heuristic(input_data):
    """
    FJSSP heuristic: Random machine selection with earliest start time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    job_current_operation = {j: 1 for j in jobs_data}

    import random

    for job_id in jobs_data:
        for op_idx, (machines, times) in enumerate(jobs_data[job_id]):
            op_num = op_idx + 1

            # Randomly select a machine from feasible machines
            chosen_machine_idx = random.randint(0, len(machines) - 1)
            machine = machines[chosen_machine_idx]
            processing_time = times[chosen_machine_idx]

            # Determine the earliest possible start time
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            # Update schedule and machine/job completion times
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
