
def heuristic(input_data):
    """Schedules jobs using a global optimization approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        current_time = 0
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            best_machine = None
            best_processing_time = float('inf')
            earliest_start = float('inf')

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_time[machine], current_time)
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine
                    best_processing_time = times[m_idx]

            start_time = max(machine_time[best_machine], current_time)
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            machine_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
