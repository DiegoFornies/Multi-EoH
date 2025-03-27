
def heuristic(input_data):
    """Schedules operations using a shortest processing time first rule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations with their possible start times
    eligible_operations = []
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, processing_times = operation
            eligible_operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'processing_times': processing_times
            })

    while eligible_operations:
        # Find the operation with the shortest processing time
        best_operation = None
        min_processing_time = float('inf')
        best_machine = None

        for operation_data in eligible_operations:
            job_id = operation_data['job_id']
            op_idx = operation_data['op_idx']
            machines = operation_data['machines']
            processing_times = operation_data['processing_times']

            for machine, processing_time in zip(machines, processing_times):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_operation = operation_data
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time


        # Schedule the operation
        job_id = best_operation['job_id']
        op_idx = best_operation['op_idx']
        start_time = best_start_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        # Remove scheduled operation from eligible list
        eligible_operations.remove(best_operation)

    return schedule
