
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes operations with fewer machine choices and shorter processing times.
    It dynamically assigns machines to minimize makespan and balance machine load.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}
    
    # Create a list of all operations, sorted by earliest possible start time
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'est': 0  # Earliest start time, initialized to 0
            })

    # Sort operations by the number of available machines (fewer first) and earliest start time
    operations.sort(key=lambda x: (len(x['machines']), x['est']))

    scheduled_operations = []

    while operations:
        operation = operations.pop(0)  # Get the highest-priority operation

        job = operation['job']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        # Find the best machine based on earliest completion time
        best_machine = None
        min_completion_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            completion_time = start_time + times[i]

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_processing_time = times[i]
        
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time

        # Update schedule
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
    
    return schedule
