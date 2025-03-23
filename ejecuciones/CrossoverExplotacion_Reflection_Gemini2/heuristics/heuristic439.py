
def heuristic(input_data):
    """Schedules jobs minimizing makespan, separation, and balancing workload.
    Dynamically adjusts balance and separation parameters based on predicted separation needs and past performance.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}
    job_start_times = {j: 0 for j in range(1, n_jobs + 1)}  # Track job start times

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    # Dynamic weight adjustment based on past performance (simplified)
    makespan_weight = 1.0
    balance_weight = 1.0
    separation_weight = 0.0  # Initially less emphasis on separation

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine = None
        min_combined_score = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine_id in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time

                # Workload balance component
                load_penalty = balance_weight * (machine_workload[machine_id] / (sum(machine_workload.values()) + 1e-6))

                # Makespan component
                makespan_penalty = makespan_weight * end_time / (max(machine_available_times.values()) + 1e-6 if machine_available_times else makespan_weight* end_time)

                # Separation component (minimize idle time between operations within a job)
                separation_benefit = 0.0
                if op_index > 0:
                    prev_op = schedule[job_id][-1]
                    separation_benefit = -separation_weight * (start_time - prev_op['End Time'])  # Negative for minimization

                combined_score = makespan_penalty + load_penalty + separation_benefit + 0.001*end_time #Tie breaker

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_job = job_id
                    best_op_index = op_index
                    best_machine = machine_id
                    best_start_time = start_time
                    best_end_time = end_time
                    best_processing_time = processing_time

        # Schedule the operation
        job_id = best_job
        op_index = best_op_index
        best_machine = best_machine
        start_time = best_start_time
        end_time = best_end_time
        processing_time = best_processing_time

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += processing_time

        if len(schedule[job_id]) == 0: #First operation
           job_start_times[job_id] = start_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

        # Dynamic weight adjustment (rudimentary)
        makespan = max(machine_available_times.values()) if machine_available_times else 0
        total_workload = sum(machine_workload.values())
        load_imbalance = sum((workload - total_workload / n_machines) ** 2 for workload in machine_workload.values())
        
        # Increase separation importance if makespan is high and load is balanced
        if makespan > 100 and load_imbalance < 10:
            separation_weight += 0.01  # Gradual increase
            separation_weight = min(separation_weight, 0.1) #Cap at 0.1

    return schedule
