
def heuristic(input_data):
    """Heuristic: SPT, load balancing, and job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_remaining_times = {j: 0 for j in jobs}

    for job_id in jobs:
        remaining_time = 0
        for machines, times in jobs[job_id]:
            remaining_time += min(times)
        job_remaining_times[job_id] = remaining_time

    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        available_operations = []
        for job_id in jobs:
            op_index = job_operations_scheduled[job_id]
            if op_index < len(jobs[job_id]):
                available_operations.append((job_id, op_index))

        if not available_operations:
            break

        best_op = None
        best_machine = None
        min_weighted_time = float('inf')

        for job_id, op_index in available_operations:
            machines, times = jobs[job_id][op_index]
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_load[machine], job_completion_times[job_id])
                end_time = start_time + processing_time
                weighted_time = end_time + 0.05 * machine_load[machine] - 0.1 * job_remaining_times[job_id]

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_op = (job_id, op_index)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        job_id, op_index = best_op
        op_num = op_index + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_load[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time
        job_remaining_times[job_id] -= best_processing_time
        job_operations_scheduled[job_id] += 1

    return schedule
