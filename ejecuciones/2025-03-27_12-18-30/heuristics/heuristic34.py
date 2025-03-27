
def heuristic(input_data):
    """Minimize makespan with machine workload balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            best_machine, best_time = None, float('inf')
            for i, machine in enumerate(machines):
                time = times[i]
                start_time = max(machine_load[machine], job_completion[job_id])
                if start_time + time < best_time:
                    best_time = start_time + time
                    best_machine = machine
                    processing_time = time
                    start = start_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start,
                'End Time': start + processing_time,
                'Processing Time': processing_time
            })
            machine_load[best_machine] = start + processing_time
            job_completion[job_id] = start + processing_time
    return schedule
