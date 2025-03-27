
def heuristic(input_data):
    """Schedules jobs by prioritizing operations with fewer machine options and shorter processing times."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize completion times for all jobs

    # Create a list of all operations for scheduling
    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_index, (machines, times) in enumerate(operations_list):
            operations.append((job_id, op_index + 1, machines, times))

    # Sort operations based on number of available machines and processing time
    operations.sort(key=lambda x: (len(x[2]), min(x[3])))  # Prioritize fewer machines, then shorter time
    
    for job_id, op_num, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')
        
        # Find best machine available, considering the processing time
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = times[i]
                best_start_time = start_time
        
        # Update schedule information
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time

    return schedule
