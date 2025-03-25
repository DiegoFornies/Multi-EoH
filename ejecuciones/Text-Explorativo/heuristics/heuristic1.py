
def heuristic(input_data):
    """
    Heuristic for FJSSP: Sorts operations by shortest processing time
    and assigns them to the machine with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a list of all operations with their possible machines and times.
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append({
                'job': job,
                'operation': op_idx + 1,
                'machines': machines,
                'times': dict(zip(machines, times))
            })

    # Sort operations by minimum processing time across all possible machines.
    operations.sort(key=lambda op: min(op['times'].values()))

    for operation in operations:
        job = operation['job']
        op_num = operation['operation']
        possible_machines = operation['machines']
        processing_times = operation['times']

        # Find the machine with the earliest available time among the possible machines.
        best_machine = None
        earliest_start_time = float('inf')
        chosen_time = 0

        for machine in possible_machines:
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                chosen_time = processing_times[machine]

        # Schedule the operation on the best machine.
        start_time = earliest_start_time
        end_time = start_time + chosen_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': chosen_time
        })

        # Update machine and job completion times.
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
