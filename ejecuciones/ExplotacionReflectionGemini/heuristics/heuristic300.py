
def heuristic(input_data):
    """Adaptive heuristic for FJSSP balancing makespan and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()
    makespan_weight = 0.5  # Initial weight, dynamically adjusted

    while available_operations:
        best_operation = None
        best_machine = None
        best_priority = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                # Calculate machine load after scheduling the operation
                future_machine_load = machine_available_time[machine] + processing_time
                
                # Prioritize machines with lower load (balance)
                balance_score = future_machine_load # Lower is better

                # Prioritize earlier start times (makespan)
                makespan_score = start_time # Lower is better
                
                # Combine makespan and balance scores
                priority = makespan_weight * makespan_score + (1 - makespan_weight) * balance_score

                if priority < best_priority:
                    best_priority = priority
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)
        
        job_id, op_idx = best_operation
        machine, processing_time = best_machine

        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))
        
        # Adaptive Adjustment (simple example: shift focus if machines are unbalanced)
        max_load = max(machine_available_time.values())
        min_load = min(machine_available_time.values())
        if max_load > 0 and (max_load - min_load) / max_load > 0.6: #Check if imbalance > 60%
            makespan_weight -= 0.05 # Reduce makespan focus
        else:
            makespan_weight += 0.025 #Increase makespan focus
        makespan_weight = max(0.1, min(makespan_weight, 0.9)) #Clamp the value

    return schedule
