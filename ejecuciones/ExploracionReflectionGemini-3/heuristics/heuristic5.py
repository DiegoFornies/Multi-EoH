
def heuristic(input_data):
    """
    A heuristic for FJSSP: Prioritizes operations with the fewest available machines,
    and schedules them on the machine that will finish earliest, reducing idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    
    remaining_operations = {job: 0 for job in range(1, n_jobs + 1)}
    for job in range(1, n_jobs + 1):
        remaining_operations[job] = len(jobs_data[job])
    
    completed_operations = {job: 0 for job in range(1, n_jobs + 1)}

    scheduled_count = 0
    total_operations = sum(remaining_operations.values())
    
    while scheduled_count < total_operations:
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if remaining_operations[job] > 0:
                op_idx = completed_operations[job]
                eligible_operations.append((job, op_idx))

        # Prioritize operations with fewer machine choices
        eligible_operations.sort(key=lambda x: len(jobs_data[x[0]][x[1]][0]))

        job, op_idx = eligible_operations[0]
        machines, times = jobs_data[job][op_idx]

        best_machine, best_time = None, float('inf')
        for m, time in zip(machines, times):
            completion_time = max(machine_available_time[m], job_completion_time[job]) + time
            if completion_time < best_time:
                best_time = completion_time
                best_machine = m

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + times[machines.index(best_machine)]
        processing_time = times[machines.index(best_machine)]
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        completed_operations[job] += 1
        remaining_operations[job] -= 1
        scheduled_count += 1

    return schedule
