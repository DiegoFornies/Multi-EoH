
def heuristic(input_data):
    """FJSSP heuristic: Combines SPT, EDD, and adaptive load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_due_dates = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize due dates
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    # Simplified EDD: Assume due date is proportional to total processing time
    for job_id in range(1, n_jobs + 1):
        total_processing_time = 0
        for operation in jobs[job_id]:
            total_processing_time += min(operation[1]) # Shortest processing time
        job_due_dates[job_id] = total_processing_time * 2 # Simple heuristic: due date is twice the total processing time

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            # Choose machine: SPT + EDD + Adaptive Load balancing
            best_machine = None
            min_score = float('inf')

            for machine in possible_machines:
                processing_time = possible_times[possible_machines.index(machine)]
                start_time = max(machine_available_time[machine], current_time)
                end_time = start_time + processing_time

                # SPT: Shorter processing time is better
                spt_score = processing_time

                # EDD: Earlier due date is better
                tardiness = max(0, end_time - job_due_dates[job_id])
                edd_score = tardiness

                # Adaptive load balancing: dynamically adjust the influence of load
                load_factor = 1 + (machine_load[machine] / sum(machine_load.values()) if sum(machine_load.values()) > 0 else 0)
                load_score = end_time * load_factor  # Penalize more loaded machines

                # Combine scores
                total_score = spt_score + edd_score + load_score
                if total_score < min_score:
                    min_score = total_score
                    best_machine = machine

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_time[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            current_time = end_time
            job_completion_time[job_id] = end_time

    return schedule
