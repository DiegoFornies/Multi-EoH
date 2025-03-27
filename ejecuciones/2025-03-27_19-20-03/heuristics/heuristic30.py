
def heuristic(input_data):
    """
    A heuristic algorithm for FJSSP minimizing makespan and balancing machine load.
    It prioritizes operations based on shortest processing time and earliest machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    operation_queue = []

    # Initialize operation queue with first operation of each job
    for job, operations in jobs_data.items():
        operation_queue.append((job, 0))  # (job_id, operation_index)

    scheduled_operations = set()

    while operation_queue:
        # Find the most suitable operation (Shortest Processing Time first)
        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_index in operation_queue:
            machines, times = jobs_data[job_id][op_index]

            # Find the best machine for this operation
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    best_processing_time = processing_time

        # Schedule the best operation
        job_id, op_index = best_operation
        machines, times = jobs_data[job_id][op_index]
        
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []
        
        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        scheduled_operations.add((job_id, op_index))

        # Add the next operation of the job to the queue if it exists
        if op_index + 1 < len(jobs_data[job_id]):
            operation_queue.append((job_id, op_index + 1))

        operation_queue.remove(best_operation)

    return schedule
