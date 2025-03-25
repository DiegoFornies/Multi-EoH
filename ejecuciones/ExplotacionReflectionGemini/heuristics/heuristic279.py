
def heuristic(input_data):
    """A dynamic heuristic balancing makespan and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    # Initialize schedule
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()
    makespan_weight = 0.5  # Initial weight for makespan
    balance_weight = 0.5  # Initial weight for balance

    while available_operations:
        best_operation = None
        best_machine = None
        best_score = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Calculate machine load after assigning this operation
                future_machine_load = machine_load[machine] + processing_time

                # Evaluate makespan impact (lower is better)
                makespan_impact = end_time

                # Evaluate balance impact (lower variance is better)
                load_values = list(machine_load.values())
                load_values[machine] += processing_time  # Simulate the assignment

                avg_load = sum(load_values) / n_machines
                balance_impact = sum([(load - avg_load) ** 2 for load in load_values])
                
                # Combine objectives with dynamic weights
                score = makespan_weight * makespan_impact + balance_weight * balance_impact

                if score < best_score:
                    best_score = score
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)
                    best_start_time = start_time
                    best_end_time = end_time

        job_id, op_idx = best_operation
        machine, processing_time = best_machine
        start_time = best_start_time
        end_time = best_end_time
        

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        machine_load[machine] += processing_time
        available_operations.remove((job_id, op_idx))

        # Add the next operation of the job if it exists
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))
            
        # Adaptive weight adjustment (simplified - can be improved)
        makespan = max(job_completion_time.values())
        load_values = list(machine_load.values())
        avg_load = sum(load_values) / n_machines
        balance = sum([(load - avg_load) ** 2 for load in load_values])

        if makespan > 100 and balance < 100:
          makespan_weight -= 0.05
          balance_weight += 0.05
        elif makespan < 100 and balance > 100:
          makespan_weight += 0.05
          balance_weight -= 0.05

        makespan_weight = max(0.1, min(0.9, makespan_weight))
        balance_weight = max(0.1, min(0.9, balance_weight))

    return schedule
