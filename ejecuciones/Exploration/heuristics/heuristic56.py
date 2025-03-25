
def heuristic(input_data):
    """Schedule jobs using a priority rule based on operation slack time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_time = {}

    # Calculate total processing time for each job
    for job in jobs:
        total_time = 0
        for op_machines, op_times in jobs[job]:
            total_time += min(op_times)  # Assume we pick fastest possible machine
        job_remaining_time[job] = total_time

    remaining_operations = {j: list(range(1, len(jobs[j]) + 1)) for j in jobs}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job in jobs:
            if remaining_operations[job]:
                op_num = remaining_operations[job][0]
                op_idx = op_num - 1
                machines, times = jobs[job][op_idx]
                eligible_operations.append((job, op_num, machines, times, job))

        if not eligible_operations:
            break

        # Prioritize operations with smallest slack time (remaining job time - shortest operation time)
        best_operation = None
        min_slack = float('inf')

        for job, op_num, machines, times, job_id in eligible_operations:
            min_op_time = min(times)
            slack_time = job_remaining_time[job_id] - min_op_time

            if slack_time < min_slack:
                min_slack = slack_time
                best_operation = (job, op_num, machines, times, job_id)

        job, op_num, machines, times, job_id = best_operation
        op_idx = op_num - 1
        
        # Find the best machine for this operation (earliest finish time)
        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None
        best_start_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time
        job_remaining_time[job_id] -= best_processing_time # Remove processing time
        remaining_operations[job_id].pop(0)

    return schedule
