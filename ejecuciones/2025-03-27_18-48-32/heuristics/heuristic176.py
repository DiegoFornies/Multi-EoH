
def heuristic(input_data):
    """Combines shortest processing time and EDD for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    job_due_time = {}
    for job in range(1, n_jobs + 1):
        job_due_time[job] = sum(min(times) for machines, times in jobs_data[job]) * 1.5

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_num, machines, times in eligible_operations:
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])
                due_time_factor = job_due_time[job] - start_time
                if due_time_factor <= 0:
                    due_time_factor = 1 #prevent negative
                priority = (times[m_idx]/due_time_factor) # prioritize shortest time and earliest due

                if start_time + priority < earliest_start:
                    earliest_start = start_time + priority
                    best_op = op_num
                    best_machine = m
                    best_time = times[m_idx]
                    best_job = job
        
        start_time = max(machine_available_time[best_machine], job_completion_time[best_job])
        end_time = start_time + best_time

        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[best_job] = end_time
        remaining_operations[best_job].pop(0)

    return scheduled_operations
