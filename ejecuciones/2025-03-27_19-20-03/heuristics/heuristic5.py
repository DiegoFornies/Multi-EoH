
def heuristic(input_data):
    """Schedules jobs minimizing idle time and balancing machine load.
    Uses Shortest Processing Time (SPT) and Earliest Start Time.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_loads = {m: 0 for m in range(n_machines)}

    # Flatten operations and associate with their job
    all_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })

    # Sort operations by Shortest Processing Time (SPT)
    all_operations.sort(key=lambda op: min(op['times']))

    for operation in all_operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        # Find the earliest possible start time on available machines
        best_machine = None
        earliest_start_time = float('inf')

        # Get last operation end time if exists for sequence feasibility
        last_op_end_time = 0
        if job_id in schedule and schedule[job_id]:
            last_op_end_time = schedule[job_id][-1]['End Time']

        for i, machine in enumerate(machines):
            processing_time = times[i]
            available_time = machine_available_times[machine]
            start_time = max(available_time, last_op_end_time)

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the chosen machine
        start_time = earliest_start_time
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,  # Operation number
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and load
        machine_available_times[best_machine] = end_time
        machine_loads[best_machine] += best_processing_time

    return schedule
