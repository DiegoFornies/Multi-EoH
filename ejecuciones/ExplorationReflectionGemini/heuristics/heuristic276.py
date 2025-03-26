
def heuristic(input_data):
    """FJSSP heuristic: Prioritizes critical operations and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    remaining_ops = {j: len(ops) for j, ops in jobs.items()}
    uncompleted_jobs = set(jobs.keys())

    while uncompleted_jobs:
        candidates = []
        for job_id in list(uncompleted_jobs):
            op_idx = len(schedule[job_id])
            machines, times = jobs[job_id][op_idx]
            candidates.append((job_id, op_idx))

        best_candidate = None
        best_priority = float('inf')

        for job_id, op_idx in candidates:
            machines, times = jobs[job_id][op_idx]
            min_start_time = float('inf')
            best_machine = None
            best_time = None

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available[machine], job_completion[job_id])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_time = time

            # Priority = (remaining_ops + processing time) / (1 + machine_load)
            priority = (remaining_ops[job_id] + best_time) / (1 + machine_available[best_machine])
            if priority < best_priority:
                best_priority = priority
                best_candidate = (job_id, op_idx, best_machine, best_time, min_start_time)

        job_id, op_idx, machine, time, start_time = best_candidate
        end_time = start_time + time
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': time
        })

        machine_available[machine] = end_time
        job_completion[job_id] = end_time
        remaining_ops[job_id] -= 1

        if remaining_ops[job_id] == 0:
            uncompleted_jobs.remove(job_id)

    return schedule
