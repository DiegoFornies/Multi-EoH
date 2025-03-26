
def heuristic(input_data):
    """Combines SPT, least loaded machine, and job urgency for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    job_remaining_work = {j: sum(min(t) for _, t in ops) for j, ops in jobs.items()}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    completed_ops = {j: 0 for j in range(1, n_jobs + 1)}

    while any(completed_ops[j] < len(jobs[j]) for j in range(1, n_jobs + 1)):
        eligible_jobs = [j for j in range(1, n_jobs + 1) if completed_ops[j] < len(jobs[j])]
        
        for job_id in eligible_jobs:
            op_index = completed_ops[job_id]
            operation_data = jobs[job_id][op_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_cost = float('inf')
            best_processing_time = None

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                # Cost: SPT + Load Balancing + Job Urgency (remaining work)
                cost = processing_time + 0.1 * machine_load[machine] - 0.01 * job_remaining_work[job_id]

                if cost < min_cost:
                    min_cost = cost
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            if best_machine is not None:
                end_time = best_start_time + best_processing_time
                schedule[job_id].append({
                    'Operation': op_index + 1,
                    'Assigned Machine': best_machine,
                    'Start Time': best_start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })

                machine_available_times[best_machine] = end_time
                machine_load[best_machine] += best_processing_time
                job_completion_times[job_id] = end_time
                job_remaining_work[job_id] -= min(possible_times) #approximation of done time
                completed_ops[job_id] += 1

    return schedule
