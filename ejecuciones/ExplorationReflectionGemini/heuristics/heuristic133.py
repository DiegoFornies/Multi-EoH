
def heuristic(input_data):
    """Greedy heuristic minimizing makespan by considering ready times and machine availability."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of operations, sorted by job then operation number.
    operations = []
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx + 1, op_data))

    while operations:
        # Find the next operation to schedule based on earliest ready time
        best_operation = None
        earliest_start = float('inf')

        for job_id, op_num, op_data in operations:
            machines, times = op_data
            job_ready_time = job_completion_time[job_id]

            # Check which machine can process the current operation at the earliest
            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_ready_time)
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine
                    processing_time = times[i]
                    best_operation = (job_id, op_num, op_data, machine, start_time, processing_time)

        # Schedule the operation
        job_id, op_num, op_data, assigned_machine, start_time, processing_time = best_operation

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[assigned_machine] = start_time + processing_time
        job_completion_time[job_id] = start_time + processing_time

        # Remove the operation from the list
        operations.remove((job_id, op_num, op_data))

    return schedule
