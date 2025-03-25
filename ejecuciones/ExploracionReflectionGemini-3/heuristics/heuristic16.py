
def heuristic(input_data):
    """A scheduling heuristic that prioritizes shortest processing time and machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    # Create a list of operations with their corresponding job, operation number, and possible machine assignments.
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op_data[0], op_data[1]))  # job_id, op_num, machines, times

    # Sort operations based on shortest processing time.
    operations.sort(key=lambda x: min(x[3]))  # Sort by minimum processing time

    for job_id, op_num, machines, times in operations:
        # Find the machine that allows the earliest completion time for the operation.
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time
        
        start_time = earliest_start_time
        end_time = start_time + best_processing_time

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        # Add the operation to the schedule.
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

    return schedule
