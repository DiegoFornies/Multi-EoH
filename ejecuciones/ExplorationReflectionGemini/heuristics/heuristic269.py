
def heuristic(input_data):
    """SPT and least loaded, dynamically selects best machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    for job in jobs:
        schedule[job] = []

    job_operations_scheduled = {job: 0 for job in jobs}
    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in jobs:
            next_op_index = job_operations_scheduled[job]
            if next_op_index >= len(jobs[job]):
                continue

            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1
            
            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_load[machine], job_completion_times[job])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            if best_machine is not None:
                start_time = max(machine_load[best_machine], job_completion_times[job])
                end_time = start_time + best_processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_times[job] = end_time
                job_operations_scheduled[job] += 1

    return schedule
