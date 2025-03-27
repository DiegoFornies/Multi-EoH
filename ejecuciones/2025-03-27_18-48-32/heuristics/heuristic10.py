
def heuristic(input_data):
    """
    Heuristic for FJSSP minimizing makespan and balancing machine load using a shortest processing time (SPT) rule.
    It considers machine availability and operation order.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_job = jobs[job_id]
        
        for op_idx, operation in enumerate(current_job):
            machines, times = operation
            
            # Find the best machine based on shortest processing time and earliest availability.
            best_machine, min_completion_time = None, float('inf')
            for m_idx, machine in enumerate(machines):
                completion_time = max(machine_available_time[machine], job_completion_time[job_id]) + times[m_idx]
                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_time = times[m_idx]
            
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_time
            
            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })
            
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += best_time
    
    return schedule
