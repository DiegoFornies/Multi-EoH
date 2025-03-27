
def heuristic(input_data):
    """Schedules jobs using a hybrid approach: FIFO and shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    job_queue = list(jobs.keys())  # FIFO job order
    
    while job_queue:
        job = job_queue.pop(0)
        if job not in schedule:
            schedule[job] = []
            
        current_time = job_completion_time[job] if job in job_completion_time else 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # SPT selection for machine assignment.
            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_time[machine], current_time)
                end_time = start_time + times[m_idx]
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[m_idx]

            start_time = max(machine_time[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = current_time

    return schedule
