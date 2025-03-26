
def heuristic(input_data):
    """Combines SPT, EST, load balancing, and job urgency for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    available_operations = []

    for job_id in jobs:
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        min_weighted_time = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]

                start_time = max(machine_load[machine], job_completion_times[job_id])
                end_time = start_time + processing_time
                weighted_time = end_time + 0.1 * machine_load[machine]
                
                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_op = op_data
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        machine_load[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
