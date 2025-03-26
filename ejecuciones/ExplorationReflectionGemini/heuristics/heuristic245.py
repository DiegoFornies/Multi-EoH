
def heuristic(input_data):
    """Dynamically adjusts priorities based on job urgency & machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_remaining_times = {j: sum(min(t) for _, t in ops) for j, ops in jobs.items()}
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        available_operations = []
        for job in jobs:
            op_index = job_operations_scheduled[job]
            if op_index < len(jobs[job]):
                available_operations.append((job, op_index))

        #Prioritize operations based on urgency (remaining time) and machine load.
        available_operations.sort(key=lambda item: job_remaining_times[item[0]] / (1 + machine_load[min(jobs[item[0]][item[1]][0])])) # Normalize and divide

        for job, op_index in available_operations:
            machines, times = jobs[job][op_index]
            op_num = op_index + 1
            best_machine, min_weighted_time, processing_time = None, float('inf'), None

            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job], machine_load[m])
                weighted_time = start_time + times[i] + 0.05 * machine_load[m] - 0.01 * job_remaining_times[job]
                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = m
                    processing_time = times[i]

            if best_machine is not None:
                start_time = max(job_completion_times[job], machine_load[best_machine])
                end_time = start_time + processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_times[job] = end_time
                job_remaining_times[job] -= processing_time
                job_operations_scheduled[job] += 1

    return schedule
