
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes jobs with fewer remaining operations
    and selects machines based on earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_current_op = {job: 0 for job in range(1, n_jobs + 1)}  # Track next operation for each job
    job_last_end_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a priority queue based on jobs with the fewest remaining operations.
    remaining_ops = {job: len(jobs_data[job]) for job in range(1, n_jobs + 1)}
    job_queue = sorted(range(1, n_jobs + 1), key=lambda job: remaining_ops[job])

    while job_queue:
        job = job_queue.pop(0)

        if job not in jobs_data or job_current_op[job] >= len(jobs_data[job]):
            continue  # Job finished or invalid

        op_idx = job_current_op[job]
        machines, times = jobs_data[job][op_idx]

        # Select machine with the earliest available time among feasible options
        best_machine, best_time = -1, float('inf')
        earliest_start = float('inf')
        
        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_available_time[machine], job_last_end_time[job])
            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = time

        if best_machine == -1:
          continue
        
        start_time = max(machine_available_time[best_machine], job_last_end_time[job])
        end_time = start_time + best_time
        op_num = op_idx + 1

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_last_end_time[job] = end_time
        job_current_op[job] += 1
        remaining_ops[job] -= 1

        # Re-sort queue based on updated remaining operations
        job_queue = sorted(job_queue, key=lambda j: remaining_ops[j] if j in remaining_ops else float('inf'))

    return schedule
