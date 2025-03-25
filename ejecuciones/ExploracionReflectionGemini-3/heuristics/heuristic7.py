
def heuristic(input_data):
    """
    Heuristic for FJSSP scheduling. Minimizes makespan and idle time 
    by prioritizing operations with fewer machine choices and shorter processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of all operations, sorted by number of possible machines (ascending)
    # and processing time (ascending).
    all_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'num_machines': len(machines)
            })

    all_operations.sort(key=lambda x: (x['num_machines'], min(x['times'])))

    # Schedule operations one by one.
    for operation in all_operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        # Find the earliest possible start time for this operation.
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = times[i]

        # Assign the operation to the selected machine and update the schedule.
        start_time = earliest_start_time
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times.
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
