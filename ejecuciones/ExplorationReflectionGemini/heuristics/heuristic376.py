
def heuristic(input_data):
    """Operation-centric scheduling, prioritizing shortest processing time and machine idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    unassigned_operations = []
    for job_id in range(1, n_jobs + 1):
        for operation_index in range(len(jobs[job_id])):
            unassigned_operations.append((job_id, operation_index))
    
    while unassigned_operations:
        # Prioritize operations with shortest processing time across all jobs
        best_operation = None
        min_processing_time = float('inf')
        
        for job_id, operation_index in unassigned_operations:
            operation_data = jobs[job_id][operation_index]
            possible_times = operation_data[1]
            if min(possible_times) < min_processing_time:
                min_processing_time = min(possible_times)
                best_operation = (job_id, operation_index)

        job_id, operation_index = best_operation
        operation_data = jobs[job_id][operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        # Schedule on machine with earliest available time
        best_machine = None
        earliest_end_time = float('inf')
        best_start_time = None
        best_processing_time = None
        
        for i in range(len(possible_machines)):
            machine = possible_machines[i]
            processing_time = possible_times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            end_time = start_time + processing_time
            
            if end_time < earliest_end_time:
                earliest_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Update schedule and machine state
        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time
        
        unassigned_operations.remove((job_id, operation_index))

    return schedule
