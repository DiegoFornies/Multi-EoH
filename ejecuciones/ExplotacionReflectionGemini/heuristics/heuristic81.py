
def heuristic(input_data):
    """FJSSP heuristic: Combines shortest processing time and earliest machine availability."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    eligible_operations = []
    for job in jobs:
        eligible_operations.append((job, 0))  # (job, operation_index)

    while eligible_operations:
        # Select operation based on shortest processing time and earliest machine availability
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]
            
            # Find the machine with the earliest available time
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = (job, op_idx)
                    best_machine = machine
                    best_processing_time = time

        # Schedule the selected operation
        job, op_idx = best_operation
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

        # Remove the scheduled operation from eligible operations
        eligible_operations.remove((job, op_idx))

        # Add the next operation of the same job to eligible operations, if any
        if op_idx + 1 < len(jobs[job]):
            eligible_operations.append((job, op_idx + 1))
            
    return schedule
