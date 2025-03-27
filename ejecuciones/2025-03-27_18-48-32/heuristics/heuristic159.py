
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}

    operations_queue = []
    for job, operations in jobs_data.items():
        operations_queue.append((0, job))  # (operation_index, job_id)
    
    while operations_queue:
        # Prioritize operations based on urgency and resource availability
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')

        for op_index, job_id in operations_queue:
            machines, times = jobs_data[job_id][op_index]
            
            for m_index, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + times[m_index]

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = (op_index, job_id)
                    best_machine = machine
                    processing_time = times[m_index]

        op_index, job_id = best_operation
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time
        scheduled_operations[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        operations_queue.remove(best_operation)

        # Add next operation to the queue
        if op_index + 1 < len(jobs_data[job_id]):
            operations_queue.append((op_index + 1, job_id))

    return scheduled_operations
