
def heuristic(input_data):
    """Heuristic for FJSSP: Random machine assignment with shortest processing time."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}


    for job in jobs:
        schedule[job] = []
        for op_idx in range(len(jobs[job])):
            machines, times = jobs[job][op_idx]

            # Randomly select a machine from the available options
            available_machines_indices = list(range(len(machines)))
            random.shuffle(available_machines_indices)

            best_machine = None
            best_time = float('inf')
            machine_index = -1

            for i in available_machines_indices:
                m = machines[i]
                t = times[i]
                if t < best_time:
                    best_time = t
                    best_machine = m
                    machine_index = i

            start_time = max(machine_time[best_machine], job_completion_time[job])
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
