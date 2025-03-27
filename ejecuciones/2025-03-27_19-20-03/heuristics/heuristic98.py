
def heuristic(input_data):
    """Heuristic for FJSSP: Random machine assignment with earliest start time."""
    import random
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}

    while any(job_ops[job] < len(jobs[job]) for job in jobs):
        for job in jobs:
            if job_ops[job] < len(jobs[job]):
                op_idx = job_ops[job]
                machines, times = jobs[job][op_idx]

                # Randomly choose a machine from the available options.
                chosen_machine_idx = random.randint(0, len(machines) - 1)
                chosen_machine = machines[chosen_machine_idx]
                processing_time = times[chosen_machine_idx]

                # Calculate the earliest possible start time for the operation.
                start_time = max(machine_time[chosen_machine], job_completion_time[job])
                end_time = start_time + processing_time

                if job not in schedule:
                    schedule[job] = []

                schedule[job].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': chosen_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                # Update machine time and job completion time.
                machine_time[chosen_machine] = end_time
                job_completion_time[job] = end_time
                job_ops[job] += 1

    return schedule
