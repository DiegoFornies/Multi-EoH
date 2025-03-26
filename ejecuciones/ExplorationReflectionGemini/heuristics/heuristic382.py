
def heuristic(input_data):
    """Combines shortest processing time and least loaded machine for FJSSP."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    
    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})
    
    while available_operations:
        best_op = None
        best_makespan = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]
            
            # Find best machine based on makespan (completion time)
            for i, machine in enumerate(machines):
                start_time = max(machine_load[machine], job_completion_times[job_id])
                end_time = start_time + times[i]
                
                if end_time < best_makespan:
                    best_makespan = end_time
                    best_op = op_data
                    best_machine = machine
                    best_processing_time = times[i]
        
        # Schedule the operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1
        
        start_time = max(machine_load[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time
        
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update data
        machine_load[best_machine] = end_time
        job_completion_times[job_id] = end_time
        
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
