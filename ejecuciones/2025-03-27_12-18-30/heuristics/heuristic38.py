
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in jobs.keys()}

    for job in jobs:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            best_machine, min_end_time = None, float('inf')

            for m_idx, machine in enumerate(machines):
                start = max(machine_available[machine], job_completion[job])
                end = start + times[m_idx]
                if end < min_end_time:
                    min_end_time = end
                    best_machine = machine
                    process_time = times[m_idx]

            start = max(machine_available[best_machine], job_completion[job])
            end = start + process_time
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start,
                'End Time': end,
                'Processing Time': process_time
            })
            machine_available[best_machine] = end
            job_completion[job] = end
    return schedule
