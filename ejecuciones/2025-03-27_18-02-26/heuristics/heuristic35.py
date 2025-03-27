
def heuristic(input_data):
    """Prioritizes jobs with more remaining operations. Schedules operations on fastest feasible machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_ops = {j: len(jobs_data[j]) for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    unscheduled_jobs = set(range(1, n_jobs + 1))

    while unscheduled_jobs:
        # Prioritize jobs with more remaining operations
        job = max(unscheduled_jobs, key=lambda j: job_remaining_ops[j])
        op_idx = len(schedule[job])  # Index of next operation
        machines, times = jobs_data[job][op_idx]
        op_num = op_idx + 1

        # Find the fastest feasible machine
        best_machine = None
        min_end_time = float('inf')

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        # Schedule the operation
        machine_available_times[best_machine] = min_end_time
        job_completion_times[job] = min_end_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })

        job_remaining_ops[job] -= 1
        if job_remaining_ops[job] == 0:
            unscheduled_jobs.remove(job)

    return schedule
