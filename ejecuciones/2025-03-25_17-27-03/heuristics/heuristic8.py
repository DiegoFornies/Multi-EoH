
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes jobs with the fewest operations,
    then selects the machine with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_ops = {j: list(range(1, len(jobs[j]) + 1)) for j in range(1, n_jobs + 1)}

    # Sort jobs by number of remaining operations
    job_priority = sorted(jobs.keys(), key=lambda j: len(job_remaining_ops[j]))
    
    while any(job_remaining_ops[j] for j in jobs.keys()):
        for job in job_priority:
            if not job_remaining_ops[job]:
                continue

            op_num = job_remaining_ops[job][0]
            op_idx = op_num - 1
            machines, times = jobs[job][op_idx]

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_available_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                available_time = max(machine_available_time[machine], job_completion_time[job])
                if available_time < min_available_time:
                    min_available_time = available_time
                    best_machine = machine
                    best_processing_time = times[i]
            
            # Schedule the operation on the selected machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time
            job_remaining_ops[job].pop(0)

    return schedule
