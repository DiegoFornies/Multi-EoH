
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes jobs with fewer remaining operations
    and selects the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_current_operation = {job: 0 for job in jobs_data}
    job_end_time = {job: 0 for job in jobs_data}
    schedule = {job: [] for job in jobs_data}
    completed_jobs = set()

    while len(completed_jobs) < n_jobs:
        eligible_jobs = {}
        for job in jobs_data:
            if job in completed_jobs:
                continue
            current_op_idx = job_current_operation[job]
            if current_op_idx < len(jobs_data[job]):
                eligible_jobs[job] = len(jobs_data[job]) - current_op_idx  # Prioritize jobs with fewer remaining ops

        if not eligible_jobs:
            break

        # Choose the job with the minimum number of remaining operations
        chosen_job = min(eligible_jobs, key=eligible_jobs.get)
        current_op_idx = job_current_operation[chosen_job]
        machines, times = jobs_data[chosen_job][current_op_idx]

        # Find the machine with the earliest available time
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_end_time[chosen_job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = times[i]

        if best_machine is None:
            print("Error: No feasible machine found!")
            return {}  # Or handle the error appropriately

        start_time = max(machine_available_time[best_machine], job_end_time[chosen_job])
        end_time = start_time + best_processing_time

        schedule[chosen_job].append({
            'Operation': current_op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_end_time[chosen_job] = end_time
        job_current_operation[chosen_job] += 1

        if job_current_operation[chosen_job] == len(jobs_data[chosen_job]):
            completed_jobs.add(chosen_job)

    return schedule
