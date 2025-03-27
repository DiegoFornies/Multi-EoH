
def heuristic(input_data):
    """Hybrid: Random machine selection with load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    import random

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Randomly select a machine from available options
            chosen_machine = random.choice(machines)
            m_idx = machines.index(chosen_machine)
            processing_time = times[m_idx]
            
            start_time = max(machine_available_time[chosen_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': chosen_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[chosen_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
