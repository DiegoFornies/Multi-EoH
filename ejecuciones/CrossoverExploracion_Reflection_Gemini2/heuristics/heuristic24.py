
def heuristic(input_data):
    """
    A heuristic that prioritizes machines with lower current load
    and operations with shorter processing times to balance load
    and reduce makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Initialize a list of operations ready to be scheduled.
    ready_operations = []
    for job_id, operations in jobs.items():
        if operations:
            ready_operations.append((job_id, 0))  # (job_id, operation_index)
    
    while ready_operations:
        # Sort operations by shortest processing time (SPT) among available machines
        ready_operations.sort(key=lambda x: min(input_data['jobs'][x[0]][x[1]][1]))
    
        job_id, op_index = ready_operations.pop(0)
        machines, times = jobs[job_id][op_index]
        
        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        min_end_time = float('inf')
        
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_time = times[i]
        
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time
        
        if job_id not in schedule:
            schedule[job_id] = []
        
        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        
        # Add next operation of the job to the ready list if it exists
        if op_index + 1 < len(jobs[job_id]):
            ready_operations.append((job_id, op_index + 1))
    
    return schedule
