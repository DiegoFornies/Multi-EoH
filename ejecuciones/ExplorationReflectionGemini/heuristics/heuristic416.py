
def heuristic(input_data):
    """Aims to minimize makespan by prioritizing operations."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    eligible_operations = []

    # Initialize eligible operations
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        eligible_operations.append((job_id, 0))  # (job_id, operation_index)

    while eligible_operations:
        # Find the most urgent operation based on estimated completion time
        best_operation = None
        min_completion_time = float('inf')

        for job_id, operation_index in eligible_operations:
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Estimate completion time for each possible machine
            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                completion_time = max(machine_available_times[machine], job_completion_times[job_id]) + processing_time
                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_operation = (job_id, operation_index, machine, processing_time)

        # Schedule the best operation
        job_id, operation_index, best_machine, best_processing_time = best_operation
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Remove the scheduled operation from eligible operations
        eligible_operations.remove((job_id, operation_index))

        # Add the next operation of the job, if any, to eligible operations
        next_operation_index = operation_index + 1
        if next_operation_index < len(jobs[job_id]):
            eligible_operations.append((job_id, next_operation_index))

    return schedule
