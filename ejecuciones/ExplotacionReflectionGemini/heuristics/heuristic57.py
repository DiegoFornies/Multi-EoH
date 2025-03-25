
def heuristic(input_data):
    """
    FJSSP heuristic: SPT job, earliest start time, machine load balancing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in jobs_data}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}
    remaining_operations = {job: len(jobs_data[job]) for job in jobs_data}
    scheduled_operations = {j: 0 for j in jobs_data}

    while any(remaining_operations[j] > 0 for j in jobs_data):
        eligible_jobs = [j for j in jobs_data if remaining_operations[j] > 0]
        if not eligible_jobs:
            break

        job = min(eligible_jobs, key=lambda j: remaining_operations[j])  # SPT job
        op_idx = scheduled_operations[job]
        machines, times = jobs_data[job][op_idx]

        best_machine, best_time, best_start_time = -1, float('inf'), float('inf')
        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < best_start_time or (start_time == best_start_time and processing_time < best_time):
                 best_machine, best_time, best_start_time = machine, processing_time, start_time

        if best_machine == -1:
            break
            
        end_time = best_start_time + best_time
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        remaining_operations[job] -= 1
        scheduled_operations[job] += 1

    return schedule
