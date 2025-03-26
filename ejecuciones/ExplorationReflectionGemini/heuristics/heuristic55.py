
def heuristic(input_data):
    """FJSSP heuristic minimizing makespan and balancing load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    
    # Prioritize jobs with more operations
    job_priority = {j: len(ops) for j, ops in jobs.items()}
    available_jobs = sorted(jobs.keys(), key=lambda j: job_priority[j], reverse=True)

    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in available_jobs:
            next_op_index = job_operations_scheduled[job]
            if next_op_index >= len(jobs[job]):
                continue
            
            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1
            
            # Choose machine with earliest finish time considering job precedence
            best_machine = None
            best_end_time = float('inf')
            processing_time = None

            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job], machine_load[m])
                end_time = start_time + times[i]
                if end_time < best_end_time:
                    best_end_time = end_time
                    best_machine = m
                    processing_time = times[i]
            
            if best_machine is not None:
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
                job_operations_scheduled[job] += 1

    return schedule
