
def heuristic(input_data):
    """Combines SPT, load balancing, and dynamic job criticality."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_remaining_times = {}

    for job, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)
        job_remaining_times[job] = total_time
    
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        # Determine job criticality dynamically
        job_priorities = {job: job_remaining_times[job] / (job_completion_times[job] + 1) for job in jobs if job_operations_scheduled[job] < len(jobs[job])}
        
        for job in sorted(job_priorities, key=job_priorities.get, reverse=True):
            next_op_index = job_operations_scheduled[job]
            if next_op_index >= len(jobs[job]):
                continue

            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1

            best_machine = None
            min_weighted_time = float('inf')
            processing_time = None

            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job], machine_load[m])
                end_time = start_time + times[i]
                weighted_time = end_time + 0.05 * machine_load[m]  # Balance makespan and load
                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = m
                    processing_time = times[i]

            start_time = max(job_completion_times[job], machine_load[best_machine])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_load[best_machine] = end_time
            job_completion_times[job] = end_time
            job_remaining_times[job] -= processing_time
            job_operations_scheduled[job] += 1

    return schedule
