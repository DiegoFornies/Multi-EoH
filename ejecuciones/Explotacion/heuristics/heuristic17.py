
def heuristic(input_data):
    """Combines least loaded machine and shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    for job_id in jobs:
        schedule[job_id] = []
        job_ops = jobs[job_id]

        for op_idx, operation in enumerate(job_ops):
            machines, times = operation
            op_num = op_idx + 1

            # Find the best machine based on combined criteria
            best_machine = None
            best_time = float('inf')
            min_end_time = float('inf')

            for i, m in enumerate(machines):
                start_time = max(machine_load[m], job_completion_times[job_id])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = m
                    best_time = times[i]


            start_time = max(machine_load[best_machine], job_completion_times[job_id])
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_load[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
