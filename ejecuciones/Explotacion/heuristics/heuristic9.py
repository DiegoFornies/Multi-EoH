
def heuristic(input_data):
    """Aims to balance machine load by scheduling operations on the least loaded machine."""
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

            # Find the least loaded machine among available machines
            best_machine = None
            min_load = float('inf')
            for i, m in enumerate(machines):
                if machine_load[m] < min_load:
                    min_load = machine_load[m]
                    best_machine = m
                    best_time = times[i]  # Correctly access the corresponding processing time

            # Schedule the operation on the best machine
            start_time = max(machine_load[best_machine], job_completion_times[job_id])
            end_time = start_time + best_time
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine load and job completion time
            machine_load[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
