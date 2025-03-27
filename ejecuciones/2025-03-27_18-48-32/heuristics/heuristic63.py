
def heuristic(input_data):
    """Minimize makespan, reduce idle time, and balance load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available = {m: 0 for m in range(n_machines)}
    job_current_time = {job: 0 for job in range(1, n_jobs + 1)}

    operations = []
    for job in range(1, n_jobs + 1):
        for op_num in range(1, len(jobs_data[job]) + 1):
            operations.append((job, op_num))

    while operations:
        best_operation = None
        earliest_end_time = float('inf')

        for job, op_num in operations:
            machines, times = jobs_data[job][op_num - 1]

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available[machine], job_current_time[job])
                end_time = start_time + times[m_idx]

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = (job, op_num)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = times[m_idx]

        job, op_num = best_operation
        operations.remove(best_operation)

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': earliest_end_time,
            'Processing Time': best_processing_time
        })

        machine_available[best_machine] = earliest_end_time
        job_current_time[job] = earliest_end_time
    
    return schedule
