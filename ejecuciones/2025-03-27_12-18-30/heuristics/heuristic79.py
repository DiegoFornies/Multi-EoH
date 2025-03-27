
def heuristic(input_data):
    """Schedules jobs using a priority rule based on operation urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    remaining_operations = {job: [(i + 1, op) for i, op in enumerate(jobs[job])] for job in range(1, n_jobs + 1)}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, ops in remaining_operations.items():
            if ops:
                eligible_operations.append((job, ops[0]))

        if not eligible_operations:
            break

        # Calculate urgency based on remaining work and due date estimation.
        operation_priorities = {}
        for job, (op_num, (machines, times)) in eligible_operations:
            min_processing_time = min(times)
            remaining_time_for_job = sum(min(times) for _, (machines, times) in remaining_operations[job])
            # Prioritize operations from jobs with less remaining work
            operation_priorities[(job, op_num)] = 1 / remaining_time_for_job if remaining_time_for_job > 0 else float('inf')


        # Select operation with the highest urgency.
        best_operation = None
        highest_priority = -1

        for (job, op_num), priority in operation_priorities.items():
           if priority > highest_priority:
              highest_priority = priority
              best_operation = (job, op_num)

        job, op_num = best_operation
        machines, times = next(op[1] for job_id, op in remaining_operations.items() if job_id == job for op_idx, op in enumerate(op) if op[0] == op_num)

        # Choose the machine that minimizes start time
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        remaining_operations[job] = [(op_number, op_data) for op_number, op_data in remaining_operations[job] if op_number != op_num] #remove scheduled operation
    return schedule
