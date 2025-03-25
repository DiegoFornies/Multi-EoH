
def heuristic(input_data):
    """
    A heuristic for FJSSP prioritizing operations with shortest processing time
    and machines with earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    
    scheduled_operations = {}
    
    # Collect all operations and their possible machines
    operations = []
    for job_id, job in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })
    
    # Sort operations based on shortest processing time (SPT) for available machine
    def sort_key(op):
        job_id = op['job_id']
        available_machines = op['machines']
        times = op['times']
        
        min_completion_time = float('inf')
        
        for i,machine in enumerate(available_machines):
            completion_time = max(machine_available_time[machine], job_completion_time[job_id]) + times[i]
            min_completion_time = min(min_completion_time,completion_time)
            
        return min_completion_time

    operations.sort(key=sort_key)
    
    # Assign operations to machines
    while operations:
        op = operations.pop(0)
        job_id = op['job_id']
        op_idx = op['op_idx']
        machines = op['machines']
        times = op['times']
        
        best_machine = None
        min_completion_time = float('inf')
        best_processing_time = None
        
        for i,machine in enumerate(machines):
            completion_time = max(machine_available_time[machine], job_completion_time[job_id]) + times[i]
            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_processing_time = times[i]

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
