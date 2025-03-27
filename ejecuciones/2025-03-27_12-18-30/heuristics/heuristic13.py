
def heuristic(input_data):
    """Schedules jobs on machines to minimize makespan using a greedy approach with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    for job in jobs:
        schedule[job] = []

    # Prioritize jobs based on the number of operations (longest job first)
    job_priority = sorted(jobs.keys(), key=lambda job: len(jobs[job]), reverse=True)

    for job in job_priority:
        job_time = 0
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Find the best machine for the operation based on earliest availability + lowest load
            best_machine = None
            min_start_time = float('inf')

            for m_idx, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = m
            
            m = best_machine
            t = times[machines.index(m)]

            start = max(machine_time[m], job_completion_time[job])
            end = start + t

            schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': t})

            machine_time[m] = end
            machine_load[m] += t
            job_completion_time[job] = end

    return schedule
