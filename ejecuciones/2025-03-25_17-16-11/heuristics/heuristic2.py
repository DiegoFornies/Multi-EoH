
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with fewer machine options and shorter processing times.
    It aims to balance machine load and minimize makespan.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data.keys()}
    schedule = {job: [] for job in jobs_data.keys()}
    
    # Create a list of operations, each operation having attributes: job, op_num, machines, times, priority
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            op_num = op_idx + 1
            # Priority is based on (number of available machines for op, minimum processing time across machines for operation)
            priority = (len(machines), min(times)) 
            operations.append({'job': job, 'op_num': op_num, 'machines': machines, 'times': times, 'priority': priority})

    # Sort the operations based on priority (fewer machines, shorter time)
    operations.sort(key=lambda x: x['priority'])

    # Schedule operations one by one
    for operation in operations:
        job = operation['job']
        op_num = operation['op_num']
        machines = operation['machines']
        times = operation['times']

        # Find the earliest available machine for the current operation
        best_machine = None
        min_start_time = float('inf')
        
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Assign the operation to the selected machine
        start_time = min_start_time
        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
    return schedule
