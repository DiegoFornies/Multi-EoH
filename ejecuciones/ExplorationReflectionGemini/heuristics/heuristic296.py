
def heuristic(input_data):
    """Schedules jobs based on operation urgency and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_remaining_work = {}

    # Initialize remaining work for each job
    for job_id, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)
        job_remaining_work[job_id] = total_time

    unscheduled_operations = []
    for job_id, operations in jobs.items():
        for op_index, op_data in enumerate(operations):
            unscheduled_operations.append((job_id, op_index))

    while unscheduled_operations:
        # Calculate urgency = remaining work of job - machine load influence
        operation_urgencies = {}
        for job_id, op_index in unscheduled_operations:
            machines, times = jobs[job_id][op_index]
            min_time = min(times)
            machine_influence = 0
            for m in machines:
                machine_influence += machine_load[m]
            operation_urgencies[(job_id, op_index)] = job_remaining_work[job_id] - 0.1 * machine_influence

        # Select the most urgent operation
        best_op = max(operation_urgencies, key=operation_urgencies.get)
        job_id, op_index = best_op
        machines, times = jobs[job_id][op_index]

        # Assign to the best machine (earliest finish time)
        best_machine = None
        earliest_finish_time = float('inf')
        processing_time = None

        for i, m in enumerate(machines):
            start_time = max(machine_load[m], job_completion_times[job_id])
            finish_time = start_time + times[i]
            if finish_time < earliest_finish_time:
                earliest_finish_time = finish_time
                best_machine = m
                processing_time = times[i]

        # Update schedule and related information
        start_time = max(machine_load[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_load[best_machine] = end_time
        job_completion_times[job_id] = end_time
        job_remaining_work[job_id] -= processing_time

        unscheduled_operations.remove((job_id, op_index))
    return schedule
