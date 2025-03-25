
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes operations with shorter processing times 
    and assigns them to machines with earlier available times to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data.keys()}
    
    # Create a list of operations with job and operation index
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[3]))
    
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the best machine based on earliest available time + processing time
        best_machine, best_time = None, float('inf')
        for i, m in enumerate(machines):
            available_time = max(machine_available_time[m], job_completion_time[job])
            completion_time = available_time + times[i]
            if completion_time < best_time:
                best_time = completion_time
                best_machine = m
                processing_time = times[i]

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
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
