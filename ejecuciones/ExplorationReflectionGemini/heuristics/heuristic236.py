
def heuristic(input_data):
    """A heuristic using a random machine assignment."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    for job_id in jobs:
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            op_num = op_idx + 1
            
            # Randomly select a machine and its processing time
            idx = random.randint(0, len(machines) - 1)
            selected_machine = machines[idx]
            selected_time = times[idx]

            # Schedule the operation
            start_time = max(machine_available_times[selected_machine], job_completion_times[job_id])
            end_time = start_time + selected_time
            
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': selected_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': selected_time
            })
            
            # Update machine availability and job completion time
            machine_available_times[selected_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
