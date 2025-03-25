
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shorter processing times and earlier machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Flatten operations into a list of tuples: (job_id, operation_index, possible_machines, processing_times)
    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job_id, op_idx, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda op: min(op[3]))  # Sort by minimum processing time across machines

    for job_id, op_idx, machines, times in operations:
        # Find the machine that allows the earliest start time for the current operation
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = times[i] # Get the correct processing time for the assigned machine

        # Schedule the operation on the best machine
        start_time = earliest_start_time
        end_time = start_time + processing_time
        operation_number = op_idx + 1

        schedule[job_id].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine available time and job completion time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
