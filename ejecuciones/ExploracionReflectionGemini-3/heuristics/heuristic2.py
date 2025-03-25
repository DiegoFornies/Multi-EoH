
def heuristic(input_data):
    """A heuristic to schedule jobs, minimizing makespan by considering machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize machine available times and job completion times
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

    # Sort operations by shortest processing time first (SPT)
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations by shortest processing time.
    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_num, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        # Find the best machine (earliest finish time) from the available machines for the operation
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[i]

        # Schedule the operation on the selected machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
