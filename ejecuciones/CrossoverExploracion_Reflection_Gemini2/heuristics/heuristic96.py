
def heuristic(input_data):
    """Schedules jobs considering machine idle time and SPT."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx))

    while operations:
        best_op = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_idx in operations:
            machines, processing_times = jobs_data[job_id][op_idx]
            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_idx)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_times[i]

        job_id, op_idx = best_op
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time
        operations.remove((job_id, op_idx))
            
    return schedule
