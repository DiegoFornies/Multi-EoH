
def heuristic(input_data):
    """
    Schedules jobs by prioritizing operations with the shortest processing time
    among available machines, minimizing makespan and machine idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Initialize a list of ready operations for each job
    ready_operations = {job: 1 for job in jobs_data}

    # Create a list of unscheduled operations
    unscheduled_operations = []
    for job, operations in jobs_data.items():
        for i in range(len(operations)):
            unscheduled_operations.append((job, i + 1))  # (job_id, operation_id)

    while unscheduled_operations:
        # Find the most suitable operation to schedule
        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job, operation_id in unscheduled_operations:
            if ready_operations[job] == operation_id:
                machines, times = jobs_data[job][operation_id - 1]
                for m_idx, machine in enumerate(machines):
                    processing_time = times[m_idx]
                    start_time = max(machine_available_time[machine], job_completion_time[job])
                    end_time = start_time + processing_time

                    if end_time < min_end_time:
                        min_end_time = end_time
                        best_operation = (job, operation_id)
                        best_machine = machine
                        best_processing_time = processing_time
                        best_start_time = start_time

        # Schedule the best operation
        job, operation_id = best_operation

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': operation_id,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = min_end_time
        job_completion_time[job] = min_end_time
        
        # Update ready operations
        ready_operations[job] += 1

        # Remove the scheduled operation from the unscheduled list
        unscheduled_operations.remove((job, operation_id))

    return schedule
