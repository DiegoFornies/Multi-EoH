
def heuristic(input_data):
    """Heuristic for FJSSP: Prioritizes shortest processing time and earliest machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Flatten the job operations into a list of schedulable operations
    schedulable_operations = []
    for job, operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations):
            schedulable_operations.append({
                'job': job,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    # Sort operations based on shortest processing time (SPT) heuristic, considering only the minimum processing time for each operation.
    schedulable_operations.sort(key=lambda op: min(op['times']))

    while schedulable_operations:
        # Select the operation to schedule based on SPT
        operation_to_schedule = schedulable_operations.pop(0)
        job = operation_to_schedule['job']
        op_num = operation_to_schedule['operation']
        machines = operation_to_schedule['machines']
        times = operation_to_schedule['times']

        # Find the machine that can start the operation the earliest
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = None

        for machine, time in zip(machines, times):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = time

        # Schedule the operation on the best machine
        start_time = earliest_start_time
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
