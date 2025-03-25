
def heuristic(input_data):
    """A heuristic for FJSSP using shortest processing time and machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))
    
    # Sort operations based on shortest processing time first
    operations.sort(key=lambda x: min(x[3]))
    
    for job, op_num, machines, times in operations:
        best_machine, best_time, start_time = None, float('inf'), 0
        
        # Find the machine with the earliest available time among feasible machines
        for i, machine in enumerate(machines):
            available_time = max(machine_available_time[machine], job_completion_time[job])
            
            if available_time + times[i] < best_time:
                best_machine, best_time = machine, available_time + times[i]
                start_time = available_time
        
        processing_time = times[machines.index(best_machine)]
        end_time = start_time + processing_time
        
        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
