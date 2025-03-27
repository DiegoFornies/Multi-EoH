
def heuristic(input_data):
    """Schedules operations based on earliest finish time, balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    remaining_operations = {job: [i for i in range(len(ops))] for job, ops in jobs.items()}

    available_operations = []
    for job in jobs:
        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0], job)) # Include job id

    while available_operations:
        # Select operation: prioritize earliest finish time
        best_op = None
        earliest_finish = float('inf')

        for op_idx, op_num, job in available_operations:
            machines, times = jobs[job][op_idx]

            for m_idx, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                end_time = start_time + times[m_idx]

                if end_time < earliest_finish:
                    earliest_finish = end_time
                    best_op = (op_idx, op_num, job, m, times[m_idx], start_time, end_time)

        op_idx, op_num, job, assigned_machine, processing_time, start_time, end_time = best_op

        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        remaining_operations[job].pop(0)
        
        machine_time[assigned_machine] = end_time
        job_completion_time[job] = end_time

        if remaining_operations[job]:
            available_operations.append((remaining_operations[job][0], job, job))

        available_operations.remove((op_idx, op_num, job))

    return schedule
