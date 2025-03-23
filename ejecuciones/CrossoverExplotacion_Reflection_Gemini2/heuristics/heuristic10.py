
def heuristic(input_data):
    """
    A heuristic algorithm for FJSSP that prioritizes shortest processing time on least loaded machine,
    dynamically updating machine load and job completion times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    
    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))  # (job_id, operation_index)

    scheduled_operations = set()

    while ready_operations:
        # Find operation with shortest processing time on least loaded machine.
        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_idx in ready_operations:
            machines, times = jobs_data[job_id][op_idx]

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_load[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job_id, op_idx)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        # Schedule the best operation
        job_id, op_idx = best_operation
        scheduled_operations.add(best_operation)
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_load[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

        # Update ready operations
        ready_operations.remove((job_id, op_idx))
        if op_idx + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_idx + 1))

    return schedule
