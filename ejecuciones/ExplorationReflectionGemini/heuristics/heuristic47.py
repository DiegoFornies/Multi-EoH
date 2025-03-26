
def heuristic(input_data):
    """Combines machine load and job precedence for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_processing_times = {}

    for job, ops in jobs.items():
        total_time = sum(min(times) for _, times in ops)
        job_processing_times[job] = total_time

    available_jobs = sorted(jobs.keys(), key=lambda x: job_processing_times[x])
    
    job_ops_scheduled = {j: 0 for j in jobs}
    while any(job_ops_scheduled[j] < len(jobs[j]) for j in jobs):
        for job in available_jobs:
            op_idx = job_ops_scheduled[job]
            if op_idx >= len(jobs[job]):
                continue

            machines, times = jobs[job][op_idx]
            op_num = op_idx + 1
            
            best_machine = None
            min_start_time = float('inf')
            proc_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[job])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    proc_time = times[i]

            if best_machine is not None:
                start_time = max(machine_time[best_machine], job_completion_time[job])
                end_time = start_time + proc_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': proc_time
                })

                machine_time[best_machine] = end_time
                job_completion_time[job] = end_time
                job_ops_scheduled[job] += 1

    return schedule
