
def heuristic(input_data):
    """Aims to minimize makespan and balance machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_jobs = {m: [] for m in range(n_machines)}

    # Flatten the jobs into a list of operations with job and op_idx information
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort the operations based on the number of possible machines (shortest first)
    operations.sort(key=lambda x: len(x[2]))

    # Iterate through the sorted operations and schedule them
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        
        # Find the best machine based on earliest completion time of the job and machine
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for m_idx, m in enumerate(machines):
            start_time = max(machine_time[m], (schedule[job][-1]['End Time'] if job in schedule and op_idx > 0 else 0 )) # respect jobs order

            if m in machine_jobs and len(machine_jobs[m]) > 0:
                start_time = max(start_time, machine_time[m])
            
            process_time = times[m_idx]
            end_time = start_time + process_time
            
            if end_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = process_time

        start_time = best_start_time
        end_time = start_time + best_processing_time
        machine_used = best_machine
        
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': machine_used,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_time[machine_used] = end_time
        machine_jobs[machine_used].append((job, op_num))
    
    return schedule
