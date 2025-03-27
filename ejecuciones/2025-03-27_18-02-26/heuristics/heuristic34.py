
def heuristic(input_data):
    """
    A heuristic for FJSSP using a priority rule based on operation slack.
    Schedules operations based on earliest due date derived from processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations, prioritized by due date (estimated)
    operations_list = []
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            # Choose the shortest processing time as the estimated processing time
            estimated_time = min(times)
            operations_list.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'estimated_time': estimated_time,
                'due_date': sum([min(jobs[job_id][i][1]) for i in range(op_idx + 1)]) # Due date: sum of estimated processing times up to this operation
            })

    # Sort operations by earliest due date
    operations_list.sort(key=lambda x: x['due_date'])

    # Schedule operations based on priority
    for operation in operations_list:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']
        
        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation
        start_time = min_start_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
