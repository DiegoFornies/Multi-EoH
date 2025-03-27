
def heuristic(input_data):
    """Schedules jobs by considering machine idle time and job waiting time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_idle_time = {m: 0 for m in range(n_machines)}
    job_wait_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Choose machine considering both machine idle time and job waiting time
            best_machine = None
            min_cost = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                cost = max(machine_idle_time[machine], job_wait_time[job]) + processing_time
                if cost < min_cost:
                    min_cost = cost
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_idle_time[best_machine], job_wait_time[job])
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_idle_time[best_machine] = end_time
            job_wait_time[job] = end_time #update job waiting time
            
    return schedule
