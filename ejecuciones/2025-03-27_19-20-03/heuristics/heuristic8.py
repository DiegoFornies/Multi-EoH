
def heuristic(input_data):
    """
    Heuristic for FJSSP: Iteratively schedules operations, prioritizing those
    with the fewest possible machines and shortest processing times, 
    while balancing machine workload.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of unscheduled operations
    unscheduled_operations = []
    for job, operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations):
            unscheduled_operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'op_num': op_idx + 1
            })

    while unscheduled_operations:
        # Prioritize operations with fewer machine options and shorter processing times
        best_op = None
        best_score = float('inf')

        for op in unscheduled_operations:
            score = len(op['machines']) + sum(op['times']) / len(op['times']) if len(op['times']) > 0 else len(op['machines'])
            if score < best_score:
                best_score = score
                best_op = op

        # Select the best machine for the chosen operation (least loaded)
        job = best_op['job']
        machines = best_op['machines']
        times = best_op['times']
        op_num = best_op['op_num']
        op_idx = best_op['op_idx']
        
        best_machine = None
        min_completion_time = float('inf')

        for m_idx, m in enumerate(machines):
            start_time = max(machine_load[m], job_completion_times[job])
            completion_time = start_time + times[m_idx]

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = m
                best_time = times[m_idx]
                start = start_time
                end = completion_time

        # Schedule the operation
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start,
            'End Time': end,
            'Processing Time': best_time
        })
        
        machine_load[best_machine] = end
        job_completion_times[job] = end

        # Remove the scheduled operation from the unscheduled list
        unscheduled_operations.remove(best_op)

    return schedule
