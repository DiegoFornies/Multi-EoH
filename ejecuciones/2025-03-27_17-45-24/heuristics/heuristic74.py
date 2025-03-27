
def heuristic(input_data):
    """Hybrid heuristic combining EFT and shortest remaining time for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_times = {}

    for job, ops in jobs_data.items():
        remaining_times[job] = sum(times[0] for _, times in ops)

    completed_operations = {job: 0 for job in range(1, n_jobs + 1)}

    while any(completed_operations[job] < len(jobs_data[job]) for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if completed_operations[job] < len(jobs_data[job]):
                eligible_operations.append(job)

        job = min(eligible_operations, key=lambda j: remaining_times[j])

        op_idx = completed_operations[job]
        machines, times = jobs_data[job][op_idx]

        best_machine = None
        min_finish_time = float('inf')
        processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]

            start_time = max(machine_availability[machine], job_completion_times[job])
            finish_time = start_time + time

            if finish_time < min_finish_time:
                min_finish_time = finish_time
                best_machine = machine
                processing_time = time

        start_time = max(machine_availability[best_machine], job_completion_times[job])
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_availability[best_machine] = end_time
        job_completion_times[job] = end_time
        remaining_times[job] -= processing_time
        completed_operations[job] += 1

    return schedule
