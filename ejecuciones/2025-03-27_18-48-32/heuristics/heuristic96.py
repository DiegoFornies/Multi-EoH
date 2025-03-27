
def heuristic(input_data):
    """FJSSP heuristic: Dynamically balances makespan and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    makespan_weight = 0.7  # Initial weight for makespan
    load_weight = 0.3  # Initial weight for machine load

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        best_operation = None
        best_score = float('inf')

        for job, op_num, machines, times in eligible_operations:
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])
                end_time = start_time + times[m_idx]
                machine_load = machine_available_time[m]  # Use available time as a proxy

                # Score combines makespan and machine load with dynamic weights
                score = makespan_weight * end_time + load_weight * machine_load

                if score < best_score:
                    best_score = score
                    best_operation = (job, op_num, m, start_time, times[m_idx])

        if best_operation:
            job, op_num, machine, start_time, processing_time = best_operation

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = start_time + processing_time
            job_completion_time[job] = start_time + processing_time

            remaining_operations[job].pop(0)
        # Adjust weights based on a simple feedback mechanism.
        # If makespan is high, reduce its weight and increase load weight.
        # This part could be further refined for a more responsive adjustment.
        total_completion_time = max(job_completion_time.values())
        if total_completion_time > 100: #threshold
            makespan_weight = max(0.2, makespan_weight - 0.05)
            load_weight = min(0.8, load_weight + 0.05)

    return schedule
