
def heuristic(input_data):
    """
    Aims to minimize makespan by prioritizing operations with shorter processing times and
    balancing machine loads.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of all operations, sorted by shortest processing time
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))
    
    # Sort operations by minimum processing time
    operations.sort(key=lambda op: min(op[3]))
    
    for job_id, op_num, machines, times in operations:
        # Find the earliest available machine for the current operation
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            available_time = machine_available_times[machine]
            job_ready_time = job_completion_times[job_id]
            start_time = max(available_time, job_ready_time)
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = times[i]

        # Schedule the operation on the best machine
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

    return schedule
