
def heuristic(input_data):
    """Schedules jobs considering machine load and job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_remaining_times = {}

    for job_id in range(1, n_jobs + 1):
        remaining_time = 0
        for machines, times in jobs[job_id]:
            remaining_time += min(times)
        job_remaining_times[job_id] = remaining_time

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        min_weighted_time = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None

            for machine_index, machine in enumerate(machines):
                processing_time = times[machine_index]
                start_time = max(machine_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Prioritize load balancing and remaining job time
                weighted_time = 0.6 * (end_time) + 0.2 * machine_time[machine] - 0.2 * job_remaining_times[job_id]

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        job_id = best_op['job']
        op_idx = best_op['op_idx']

        machine_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time
        job_remaining_times[job_id] -= best_processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
