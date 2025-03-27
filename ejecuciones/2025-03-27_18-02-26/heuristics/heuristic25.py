
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    It prioritizes operations based on shortest processing time (SPT) and
    earliest machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    scheduled_operations = {}

    # Create a list of all operations with their potential start times
    eligible_operations = []
    for job_id, operations in jobs.items():
        scheduled_operations[job_id] = []
        eligible_operations.append((job_id, 0))  # (job_id, operation_index)

    # Main scheduling loop
    while eligible_operations:
        # Find the operation with the shortest possible processing time
        best_op = None
        best_machine = None
        earliest_start_time = float('inf')
        shortest_processing_time = float('inf')

        for job_id, op_index in eligible_operations:
            machines, times = jobs[job_id][op_index]

            for machine_index, processing_time in enumerate(times):
                machine = machines[machine_index]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if processing_time < shortest_processing_time or (processing_time == shortest_processing_time and start_time < earliest_start_time):
                    shortest_processing_time = processing_time
                    earliest_start_time = start_time
                    best_op = (job_id, op_index)
                    best_machine = machine
                    best_processing_time = processing_time

        # Schedule the best operation
        job_id, op_index = best_op
        scheduled_operations[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': earliest_start_time,
            'End Time': earliest_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = earliest_start_time + best_processing_time
        job_completion_time[job_id] = earliest_start_time + best_processing_time

        # Remove the scheduled operation from eligible operations
        eligible_operations.remove(best_op)

        # Add the next operation of the job to eligible operations if it exists
        if op_index + 1 < len(jobs[job_id]):
            eligible_operations.append((job_id, op_index + 1))

    return scheduled_operations
