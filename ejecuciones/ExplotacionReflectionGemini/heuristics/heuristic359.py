
def heuristic(input_data):
    """Adaptive heuristic balancing makespan and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Initialize schedule
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # Create a list of operations to schedule
    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    # Parameters for adaptive balancing
    makespan_weight = 0.7  # Initial weight for makespan
    balance_weight = 0.3   # Initial weight for machine balance
    adaptive_factor = 0.05 # Adjusts the weights

    while available_operations:
        best_operation = None
        best_machine = None
        best_score = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                # Calculate makespan component
                makespan_contribution = start_time + processing_time

                # Calculate balance component (idle time until next job)
                balance_contribution = machine_available_time[machine]

                # Calculate combined score
                score = makespan_weight * makespan_contribution + balance_weight * balance_contribution

                if score < best_score:
                    best_score = score
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)
                    best_start_time = start_time

        job_id, op_idx = best_operation
        machine, processing_time = best_machine
        start_time = best_start_time

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

        # Add the next operation of the job if it exists
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

        # Adaptive adjustment of weights (Simplified)
        # Check if the assigned machine is becoming overloaded
        machine_load = machine_available_time[machine]
        avg_machine_load = sum(machine_available_time.values()) / n_machines

        if machine_load > avg_machine_load:
            # Shift focus towards balancing
            makespan_weight = max(0.1, makespan_weight - adaptive_factor)
            balance_weight = min(0.9, balance_weight + adaptive_factor)
        else:
            # Shift focus towards makespan
            makespan_weight = min(0.9, makespan_weight + adaptive_factor)
            balance_weight = max(0.1, balance_weight - adaptive_factor)

    return schedule
