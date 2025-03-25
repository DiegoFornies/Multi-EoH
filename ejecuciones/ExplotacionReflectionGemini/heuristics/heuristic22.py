
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules jobs based on shortest processing time (SPT)
    and earliest available machine to minimize makespan and balance load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}  # Track completion time for each job

    # Initialize a list of operations for each job
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op))

    # Sort operations based on shortest processing time first
    operations.sort(key=lambda x: min(x[2][1]))

    for job_id, op_num, op_data in operations:
        machines, times = op_data

        # Find the machine that becomes available the soonest with the shortest processing time
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id]) # ensure both sequence and machine feasibility
            end_time = start_time + processing_time
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        # Update schedule
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

    return schedule
