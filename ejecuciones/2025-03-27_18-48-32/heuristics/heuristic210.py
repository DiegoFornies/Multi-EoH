
def heuristic(input_data):
    """Schedules jobs considering machine load and operation urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    remaining_operations = {job: len(ops) for job, ops in jobs_data.items()}

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]
            remaining_time_current_job = 0
            for i in range(op_num, len(jobs_data[job]) + 1):
                if i <= len(jobs_data[job]):
                    machines_next, times_next = jobs_data[job][i-1]
                    remaining_time_current_job += min(times_next)

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                machine_load_penalty = machine_available_times[m] # penalize busy machines
                urgency = remaining_time_current_job # prioritize jobs with less remaining time

                weighted_start_time = start_time + machine_load_penalty - urgency/10

                if weighted_start_time < earliest_start:
                    earliest_start = weighted_start_time
                    best_op = op_num
                    best_machine = m
                    best_time = times[m_idx]
                    best_job = job
        
        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_time
        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[best_job] = end_time

        eligible_operations.remove((best_job, best_op))
        
        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
