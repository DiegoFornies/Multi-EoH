
def heuristic(input_data):
    """Schedules operations based on shortest processing time and earliest machine availability."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Tracks the completion time of each job
    schedule = {}

    # Initialize the schedule dictionary
    for job in range(1, n_jobs + 1):
        schedule[job] = []

    # Create a list of operations to schedule
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job, op_idx + 1, machines, times))

    # Sort the operations based on shortest processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        best_machine = -1
        min_end_time = float('inf')
        processing_time = -1

        # Find the best machine for the operation
        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = time

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
