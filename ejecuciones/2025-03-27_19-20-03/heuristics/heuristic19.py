
def heuristic(input_data):
    """Heuristic for FJSSP: Prioritize operations with fewer machine choices and shorter processing times."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of all operations, along with their job and operation index
    all_operations = []
    for job_id, operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    # Sort operations by number of possible machines and processing time
    all_operations.sort(key=lambda op: (len(op['machines']), sum(op['times'])))

    # Schedule operations
    for operation_data in all_operations:
        job_id = operation_data['job']
        operation_num = operation_data['operation']
        machines = operation_data['machines']
        times = operation_data['times']

        # Find the earliest available machine and corresponding start time
        best_machine = None
        min_start_time = float('inf')
        processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = time

        # Schedule the operation on the best machine
        start_time = min_start_time
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': operation_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
