
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with fewer machine choices
    and shortest processing times to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations with job, operation index, machines, and times
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append({
                'job': job,
                'operation_index': op_idx,
                'machines': machines,
                'times': times
            })

    # Sort operations: prioritizing fewer machine options and shorter processing times
    operations.sort(key=lambda x: (len(x['machines']), min(x['times'])))

    for operation in operations:
        job = operation['job']
        op_idx = operation['operation_index']
        machines = operation['machines']
        times = operation['times']
        
        # Choose the machine with earliest available time for this operation
        best_machine = None
        min_end_time = float('inf')
        
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + times[i]
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = times[i]

        # Update schedule
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time

    return schedule
