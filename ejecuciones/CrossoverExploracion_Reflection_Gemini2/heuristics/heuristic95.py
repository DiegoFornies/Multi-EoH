
def heuristic(input_data):
    """Schedules operations using a shortest processing time and least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, processing_times = operation
            op_num = op_idx + 1
            
            # Find the shortest processing time for feasible machines
            shortest_time = float('inf')
            best_machine = None
            for m, time in zip(machines, processing_times):
                if time < shortest_time:
                    shortest_time = time
                    best_machine = m

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + shortest_time
            
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': shortest_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += shortest_time

    return schedule
