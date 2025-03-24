
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes short processing times and machine availability
    to minimize makespan and idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    for job in jobs:
        schedule[job] = []

    operations_remaining = {job: list(range(1, len(jobs[job]) + 1)) for job in jobs}

    scheduled_operations = set()
    
    while any(operations_remaining.values()):
        
        eligible_operations = []
        for job in jobs:
            if operations_remaining[job]:
                op_idx = operations_remaining[job][0] - 1
                eligible_operations.append((job, op_idx + 1))

        # Select the best operation based on heuristic criteria
        best_operation = None
        best_makespan = float('inf')
        
        for job, op_num in eligible_operations:
            op_idx = op_num - 1
            machines, times = jobs[job][op_idx]
            
            # Find the earliest available machine for this operation
            earliest_start = float('inf')
            selected_machine = None
            selected_time = None

            for m, t in zip(machines, times):
                start_time = max(machine_availability[m], job_completion_times[job])
                if start_time < earliest_start:
                    earliest_start = start_time
                    selected_machine = m
                    selected_time = t
            
            # Estimated makespan if this operation is scheduled now
            estimated_makespan = earliest_start + selected_time

            if estimated_makespan < best_makespan:
                best_makespan = estimated_makespan
                best_operation = (job, op_num, selected_machine, earliest_start, selected_time)

        if best_operation:
            job, op_num, machine, start_time, processing_time = best_operation
            
            end_time = start_time + processing_time
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            
            machine_availability[machine] = end_time
            job_completion_times[job] = end_time
            operations_remaining[job].pop(0)
    
    return schedule
