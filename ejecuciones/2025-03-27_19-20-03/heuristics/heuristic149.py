
def heuristic(input_data):
    """Schedules jobs using a random machine selection with makespan consideration."""
    import random
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs_data:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Randomly select a machine from available options.
            chosen_machine_idx = random.randint(0, len(machines) - 1)
            machine = machines[chosen_machine_idx]
            processing_time = times[chosen_machine_idx]

            # Schedule the operation.
            start_time = max(machine_available_time[machine], current_time)
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times.
            machine_available_time[machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
