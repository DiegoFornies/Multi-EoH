
def heuristic(input_data):
    """FJSSP heuristic: SPT, EDD, and adaptive load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_due_dates = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    # Estimate job due dates (EDD component)
    for job, operations in jobs_data.items():
        total_processing_time = 0
        for op_idx, operation in enumerate(operations):
            min_time = min(operation[1])  # SPT for initial due date
            total_processing_time += min_time
        job_due_dates[job] = total_processing_time * 1.5  # Due date is 1.5x est. time

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        best_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]
            
            best_local_machine = None
            best_local_start = float('inf')
            best_local_time = None

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], sum([op['Processing Time'] for op in scheduled_operations[job]]))

                # Adaptive priority: load, EDD, and SPT
                load_penalty = machine_load[m] * 0.1
                due_date_bonus = (job_due_dates[job] - start_time) / job_due_dates[job] if job_due_dates[job] > 0 else 0
                spt_bonus = times[m_idx] * 0.02 # shorter processing time machine selection. 

                adjusted_start_time = start_time + load_penalty - (due_date_bonus * 25) + spt_bonus

                if adjusted_start_time < best_local_start:
                    best_local_start = adjusted_start_time
                    best_local_machine = m
                    best_local_time = times[m_idx]

            if best_local_start < best_start:
                best_start = best_local_start
                best_op = op_num
                best_machine = best_local_machine
                best_time = best_local_time
                best_job = job

        start_time = max(machine_available_times[best_machine], sum([op['Processing Time'] for op in scheduled_operations[best_job]]))
        end_time = start_time + best_time

        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_times[best_machine] = end_time
        machine_load[best_machine] += best_time

        eligible_operations.remove((best_job, best_op))

        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
