
def heuristic(input_data):
    """Combines EDD and SPT for FJSSP, balancing makespan and load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    job_due_time = {}
    for job in range(1, n_jobs + 1):
        job_due_time[job] = sum(min(times) for machines, times in jobs_data[job]) * 1.5

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None
        best_edd = float('inf')

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                if start_time < earliest_start or \
                   (start_time == earliest_start and job_due_time[job] < best_edd):
                    earliest_start = start_time
                    best_op = op_num
                    best_machine = m
                    best_time = times[m_idx]
                    best_job = job
                    best_edd = job_due_time[job]

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
