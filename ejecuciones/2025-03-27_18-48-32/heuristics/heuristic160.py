
def heuristic(input_data):
    """Schedules jobs to minimize makespan and balance machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    
    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))
        
    while eligible_operations:
        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None
        
        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]
            
            # Prioritize lightly loaded machines.
            machine_scores = {}
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                machine_scores[m] = start_time + times[m_idx] # weighted by completion
            
            # Find the best available machine based on the scores, and start time
            sorted_machines = sorted(machine_scores.items(), key=lambda item: item[1])
            for m,score in sorted_machines:
                m_idx = machines.index(m)
                start_time = max(machine_available_times[m], job_completion_times[job])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = op_num
                    best_machine = m
                    best_time = times[m_idx]
                    best_job = job

        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_time
        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[best_job] = end_time
        
        eligible_operations.remove((best_job, best_op))
        
        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
