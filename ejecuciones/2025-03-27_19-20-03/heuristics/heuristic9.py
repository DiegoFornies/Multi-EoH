
def heuristic(input_data):
    """A heuristic to solve FJSSP, minimizing makespan."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize machine availability times and job completion times
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    # Heuristic: Prioritize operations with the shortest processing time
    # on the least loaded machine.

    # Create a list of all operations with their possible machines and times
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,  # Operation number
                'machines': machines,
                'times': times
            })

    # Sort operations based on the shortest processing time
    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        # Find the machine with the earliest available time among the possible machines
        best_machine = None
        min_start_time = float('inf')
        processing_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_availability[machine], job_completion_times[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = times[i]

        # Schedule the operation on the best machine
        start_time = min_start_time
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_availability[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
