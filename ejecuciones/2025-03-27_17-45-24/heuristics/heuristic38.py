
def heuristic(input_data):
    """
    A hybrid heuristic for FJSSP combining Shortest Processing Time (SPT) and
    Earliest Due Date (EDD) principles to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations with job and operation IDs
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, operation_data in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx + 1, operation_data))

    # Sort operations based on Shortest Processing Time (SPT)
    operations.sort(key=lambda x: min(x[2][1]))  # Sort by shortest possible processing time

    for job_id, op_num, operation_data in operations:
        machines, times = operation_data
        best_machine = None
        min_end_time = float('inf')

        # Find the machine that minimizes the completion time for the operation
        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time
        
        # Assign the operation to the best machine
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

    return schedule
