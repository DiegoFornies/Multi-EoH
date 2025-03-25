
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations based on the shortest processing time
    and earliest available machine to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of operations, each associated with its job
    operations = []
    for job_id, job in jobs_data.items():
        for op_idx, op in enumerate(job):
            operations.append((job_id, op_idx, op))
    
    # Sort operations based on shortest processing time available
    operations.sort(key=lambda x: min(x[2][1]))
    
    for job_id, op_idx, op in operations:
        machines, times = op

        # Find the machine that allows the earliest start time
        best_machine, min_start_time = None, float('inf')
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = times[i] #Select correct time for machine.
                
        start_time = min_start_time
        end_time = start_time + processing_time
        
        # Update schedule
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        
    return schedule
