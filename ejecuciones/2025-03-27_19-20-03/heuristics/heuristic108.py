
def heuristic(input_data):
    """Prioritizes jobs randomly and assigns operations to the first available machine."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    job_order = list(jobs_data.keys())
    random.shuffle(job_order)  # Randomize job order

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            machine = machines[0]  # Assign to the first feasible machine
            processing_time = times[0] #Take the first time related

            start_time = max(machine_available_time[machine], current_time)
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
