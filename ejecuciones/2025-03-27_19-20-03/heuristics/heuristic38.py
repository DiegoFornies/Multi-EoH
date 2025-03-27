
def heuristic(input_data):
    """Heuristic for FJSSP: Random machine selection."""
    n_jobs = input_data['n_jobs']
    jobs_data = input_data['jobs']
    schedule = {}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        current_time = 0
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation
            import random
            m_idx = random.randint(0, len(machines) - 1)
            machine = machines[m_idx]
            processing_time = times[m_idx]

            start_time = current_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            current_time = end_time
    return schedule
