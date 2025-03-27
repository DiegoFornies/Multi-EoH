
def heuristic(input_data):
    """A heuristic for FJSSP that minimizes makespan using a greedy approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            best_machine = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[job])
                end_time = start_time + times[m_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    processing_time = times[m_idx]

            machine_time[best_machine] = min_end_time
            job_completion_time[job] = min_end_time
            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': processing_time
            })

    return schedule
