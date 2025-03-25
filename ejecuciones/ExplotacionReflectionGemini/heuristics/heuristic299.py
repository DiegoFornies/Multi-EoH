
def heuristic(input_data):
    """Adaptive heuristic balancing makespan and machine load."""
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
                
                #Heuristic Scoring
                makespan_impact = end_time #End time can represent makespan contribution
                load_impact = 0 #load impact
                for m in range(n_machines):
                    load_impact+=machine_available_time[m]
                
                load_impact = load_impact/n_machines if n_machines > 0 else 0

                score = makespan_weight * makespan_impact + balance_weight * machine_available_time[machine]

                if score < best_score:
                    best_score = score
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)
                    best_start_time = start_time #Used for scheduling

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

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))
            
        #Adaptive Adjustment of weights
        makespan_weight *= 0.99 #Reduce weight for make span
        balance_weight = 1 - makespan_weight

    return schedule
