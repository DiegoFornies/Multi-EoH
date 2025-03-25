
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shortest processing time and minimizes machine idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations, prioritizing them based on the shortest processing time
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations by the minimum processing time among available machines
    operations.sort(key=lambda op: min(op[3]))  # Sort based on shortest processing time

    for job_id, op_num, machines, times in operations:
        # Find the machine that allows the earliest start time for the operation
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = times[m_idx]

        # Schedule the operation on the selected machine
        start_time = earliest_start_time
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

        # Update machine availability and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
