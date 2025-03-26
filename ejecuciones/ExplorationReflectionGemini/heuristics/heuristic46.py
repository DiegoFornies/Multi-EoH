
def heuristic(input_data):
    """Combines machine load and job precedence for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_operation_scheduled = {j: 0 for j in jobs}

    while any(job_operation_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in jobs:
            op_idx = job_operation_scheduled[job]
            if op_idx >= len(jobs[job]):
                continue

            machines, times = jobs[job][op_idx]
            op_num = op_idx + 1
            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            for i, m in enumerate(machines):
                start_time = max(machine_load[m], job_completion_time[job])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = m
                    processing_time = times[i]
            
            if best_machine is not None:
                start_time = max(machine_load[best_machine], job_completion_time[job])
                end_time = start_time + processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_time[job] = end_time
                job_operation_scheduled[job] += 1

    return schedule
