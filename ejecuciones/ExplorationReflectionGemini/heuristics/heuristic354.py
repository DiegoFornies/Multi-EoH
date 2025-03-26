
def heuristic(input_data):
    """Schedules jobs considering machine idle time and job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_ready = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Job Urgency: Based on number of remaining operations.
    job_urgency = {j: len(jobs[j]) for j in jobs}

    unscheduled_operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(jobs[job_id])):
            unscheduled_operations.append((job_id, op_idx))

    while unscheduled_operations:
        best_op = None
        best_machine = None
        min_start_time = float('inf')

        eligible_ops = []
        for job_id, op_idx in unscheduled_operations:
            if op_idx == 0 or schedule[job_id][-1]['Operation'] == op_idx:
                eligible_ops.append((job_id, op_idx))

        # Prioritize operations based on urgency and machine availability.
        for job_id, op_idx in eligible_ops:
            machines, times = jobs[job_id][op_idx]

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available[machine], job_ready[job_id])
                
                # Job urgency increases priority when machines are equally available.
                # Reduces idle time by considering job urgency.
                cost = start_time - 0.1 * job_urgency[job_id]

                if cost < min_start_time:
                    min_start_time = cost
                    best_op = (job_id, op_idx)
                    best_machine = machine
                    best_processing_time = processing_time

        if best_op is not None:
            job_id, op_idx = best_op
            machines, times = jobs[job_id][op_idx]
            processing_time = best_processing_time
            start_time = max(machine_available[best_machine], job_ready[job_id])
            end_time = start_time + processing_time

            if job_id not in schedule:
                schedule[job_id] = []

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            
            machine_available[best_machine] = end_time
            job_ready[job_id] = end_time
            job_urgency[job_id] -=1

            unscheduled_operations.remove((job_id, op_idx))
        else:
            break  # No eligible operations

    return schedule
