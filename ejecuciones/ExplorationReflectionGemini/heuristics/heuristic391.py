
def heuristic(input_data):
    """Combines earliest start time, SPT, and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_total_processing_times = {}

    for job, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)
        job_total_processing_times[job] = total_time

    available_jobs = sorted(list(jobs.keys()), key=lambda x: job_total_processing_times[x])
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in available_jobs:
            next_op_index = job_operations_scheduled[job]

            if next_op_index >= len(jobs[job]):
                continue

            possible_machines = jobs[job][next_op_index][0]
            possible_times = jobs[job][next_op_index][1]
            op_num = next_op_index + 1

            best_machine = None
            min_weighted_time = float('inf')
            best_processing_time = None

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                start_time = max(machine_load[machine], job_completion_time[job])
                end_time = start_time + processing_time

                weighted_time = end_time + 0.1 * machine_load[machine]

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            if best_machine is not None:
                start_time = max(machine_load[best_machine], job_completion_time[job])
                end_time = start_time + best_processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_time[job] = end_time
                job_operations_scheduled[job] += 1

    return schedule
