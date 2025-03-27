
def heuristic(input_data):
    """
    Heuristic scheduling algorithm for FJSSP focusing on minimizing idle time and balancing machine load.
    Prioritizes operations based on shortest processing time and machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Collect operations for scheduling in a list of tuples: (job_id, op_index, machines, times)
    operations = []
    for job_id, job_ops in jobs.items():
        for op_index, op_data in enumerate(job_ops):
            operations.append((job_id, op_index + 1, op_data[0], op_data[1]))

    # Sort operations by shortest processing time first, and job id second
    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_num, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')

        for machine_index, machine in enumerate(machines):
            processing_time = times[machine_index]
            available_time = machine_available_times[machine]
            job_ready_time = job_completion_times[job_id]
            
            start_time = max(available_time, job_ready_time)
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time
                

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

    return schedule
