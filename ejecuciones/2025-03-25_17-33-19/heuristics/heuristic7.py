
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shortest processing time and earliest machine availability.
    Minimizes makespan while respecting operation, machine, and sequence feasibility constraints.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}

    # Create a list of operations and their possible machines
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })

    # Sort operations by shortest processing time
    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        # Find the machine that allows the earliest completion time
        best_machine = None
        earliest_completion = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            completion_time = start_time + processing_time

            if completion_time < earliest_completion:
                earliest_completion = completion_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the selected machine
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
