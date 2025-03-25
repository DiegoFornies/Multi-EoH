
def heuristic(input_data):
    """
    A heuristic for FJSSP scheduling that considers machine load and operation urgency.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule, machine availability, and job completion times
    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    # Create a list of operations to schedule, with urgency based on remaining work
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by job number and operation number to preserve order
    operations.sort(key=lambda x: (x[0], x[1]))

    # Schedule operations
    while operations:
        # Find the most urgent operation (shortest processing time on available machine)
        best_op = None
        best_machine = None
        min_end_time = float('inf')

        for job, op_idx, machines, times in operations:
            # Consider the available machines for this operation
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = available_time + processing_time

                # Select the best machine based on the earliest end time
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job, op_idx, machines, times)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_available_time = available_time

        # Schedule the operation on the selected machine
        job, op_idx, machines, times = best_op
        op_num = op_idx + 1

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_available_time,
            'End Time': best_available_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = best_available_time + best_processing_time
        job_completion_time[job] = best_available_time + best_processing_time
        
        # Remove scheduled operation
        operations.remove(best_op)

    return schedule
