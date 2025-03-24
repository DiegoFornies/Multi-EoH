
def heuristic(input_data):
    """
    Heuristic for FJSSP that prioritizes operations based on shortest processing time
    and earliest available machine. Uses a greedy approach to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of operations, prioritizing by shortest processing time
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })
    
    # Sort operations by minimum processing time
    operations.sort(key=lambda op: min(op['times']))
    
    for operation in operations:
        job = operation['job']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']
        op_num = op_idx + 1
        
        # Find the earliest available machine among feasible machines
        best_machine = None
        min_start_time = float('inf')
        
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_time_index = i

        if best_machine is None:
            # Handle cases where all feasible machines are blocked (rare, but possible)
            best_machine = machines[0]  # Fallback to the first machine
            best_time_index = 0
            min_start_time = max(machine_available_time[best_machine], job_completion_time[job])

        processing_time = times[best_time_index]
        start_time = min_start_time
        end_time = start_time + processing_time

        # Update schedule and machine/job completion times
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
