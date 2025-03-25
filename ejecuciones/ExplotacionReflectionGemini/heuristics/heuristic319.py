
def heuristic(input_data):
    """FJSSP heuristic: Adapts between makespan and balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()

    while available_operations:
        best_operation = None
        best_machine = None
        best_start_time = float('inf')
        makespan_weight = 0.6  # Initial weight for makespan
        balance_weight = 0.4   # Initial weight for balance

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                # Calculate machine load after assigning this operation
                future_load = machine_load[machine] + processing_time

                # Evaluate cost based on weighted makespan and balance
                makespan_cost = start_time
                balance_cost = future_load  # Simpler load metric

                # Weighted cost
                cost = makespan_weight * makespan_cost + balance_weight * balance_cost

                if cost < best_start_time:
                    best_start_time = cost
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
        machine_load[machine] += processing_time
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

        # Adapt weights: Reduce makespan weight if machines are unbalanced
        load_values = list(machine_load.values())
        load_range = max(load_values) - min(load_values) if load_values else 0 # Avoid ZeroDivisionError if no jobs

        if load_range > sum(load_values) / n_machines / 2:  # Adjust threshold based on average load
            makespan_weight = max(0.2, makespan_weight - 0.05) # Min makespan weight=0.2
            balance_weight = min(0.8, balance_weight + 0.05) # Max balance weight=0.8
            
    return schedule
