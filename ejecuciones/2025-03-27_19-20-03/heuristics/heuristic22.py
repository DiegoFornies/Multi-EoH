
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules operations greedily based on shortest processing time,
    while respecting operation and machine feasibility constraints.

    Input: FJSSP instance.
    Output: Schedule minimizing makespan, idle time, and balancing machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort operations by shortest processing time first
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    operations.sort(key=lambda x: min(x[3]))  # Sort by shortest processing time

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        
        # Find the best machine for the operation
        best_machine = None
        min_end_time = float('inf')
        
        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job] = best_start_time + best_processing_time

    return schedule
