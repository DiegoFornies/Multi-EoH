
def heuristic(input_data):
    """Heuristic: Random machine assignment + earliest start time."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            # Randomly assign machine
            m_idx = random.randint(0, len(machines) - 1)
            machine = machines[m_idx]
            processing_time = times[m_idx]

            # Calculate earliest start time
            start_time = max(machine_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_time[machine] = end_time
            job_completion_time[job] = end_time

    return schedule
