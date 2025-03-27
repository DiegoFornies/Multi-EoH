
def heuristic(input_data):
    """Schedules operations based on earliest start time, minimizing makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations with their earliest possible start times
    eligible_operations = []
    for job_id in range(1, n_jobs + 1):
        eligible_operations.append((job_id, 0))  # (job_id, operation_index)

    while eligible_operations:
        best_operation = None
        earliest_start_time = float('inf')

        # Find the operation with the earliest possible start time
        for job_id, op_index in eligible_operations:
            operation = jobs[job_id][op_index]
            eligible_machines = operation[0]
            processing_times = operation[1]

            for machine_index, machine_id in enumerate(eligible_machines):
                machine_start_time = machine_available_time[machine_id]
                job_start_time = job_completion_time[job_id]
                start_time = max(machine_start_time, job_start_time)

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_operation = (job_id, op_index, machine_id, processing_times[machine_index], start_time)

        # Schedule the best operation
        job_id, op_index, machine_id, processing_time, start_time = best_operation
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': machine_id,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[machine_id] = end_time
        job_completion_time[job_id] = end_time

        # Add the next operation for the job to the eligible operations list
        if op_index + 1 < len(jobs[job_id]):
            eligible_operations.append((job_id, op_index + 1))

        eligible_operations.remove((job_id, op_index))

    return schedule
