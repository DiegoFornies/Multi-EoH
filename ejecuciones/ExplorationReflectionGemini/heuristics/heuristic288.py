
def heuristic(input_data):
    """Earliest start time + machine load balancing + job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    job_remaining_work = {j: sum(min(t) for _, t in ops) for j, ops in jobs.items()}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    scheduled_ops = {job_id: 0 for job_id in range(1, n_jobs + 1)}

    while any(scheduled_ops[job_id] < len(jobs[job_id]) for job_id in range(1, n_jobs + 1)):
        eligible_ops = []
        for job_id in range(1, n_jobs + 1):
            if scheduled_ops[job_id] < len(jobs[job_id]):
                eligible_ops.append(job_id)

        # Prioritize jobs with the least remaining work (job urgency)
        eligible_ops = sorted(eligible_ops, key=lambda j: job_remaining_work[j])

        for job_id in eligible_ops:
            operation_index = scheduled_ops[job_id]
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_weighted_time = float('inf')
            best_start_time = 0
            best_processing_time = 0
           
            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                start_time = max(machine_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Prioritize machines with lower load and earlier completion
                weighted_time = end_time + 0.1 * machine_load[machine]

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time
            job_remaining_work[job_id] -= best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            scheduled_ops[job_id] += 1

    return schedule
