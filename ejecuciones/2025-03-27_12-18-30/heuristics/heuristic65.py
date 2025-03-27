
def heuristic(input_data):
    """Schedule jobs minimizing makespan using a hybrid approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job in range(1, n_jobs + 1):
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        best_machine = None
        min_end_time = float('inf')
        
        for job, op_num in eligible_operations:
            if op_num > len(jobs[job]):
                continue
            machines, times = jobs[job][op_num - 1]
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job, op_num)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time
        
        if best_op:
            job, op_num = best_op
            start_time = best_start_time
            end_time = start_time + best_processing_time
            machine = best_machine
            processing_time = best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            
            machine_available_time[machine] = end_time
            job_completion_time[job] = end_time

            eligible_operations.remove((job, op_num))
            if op_num + 1 <= len(jobs[job]):
                 eligible_operations.append((job, op_num + 1))
                    
    return schedule
