
def heuristic(input_data):
    """Combines EDD and SPT with dynamic machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_due_time = {}
    for job in range(1, n_jobs + 1):
        job_due_time[job] = sum(min(times) for machines, times in jobs_data[job]) * 1.5

    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: list(range(1, len(jobs_data[job]) + 1)) for job in range(1,n_jobs + 1)}

    machine_load = {m: 0 for m in range(n_machines)}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if remaining_operations[job]:
                op_num = remaining_operations[job][0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times, job_due_time[job]))

        best_op = None
        best_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_num, machines, times, due_time in eligible_operations:
            best_local_machine = None
            best_local_start = float('inf')
            best_local_time = None

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])

                load_penalty = machine_load[m] * 0.05
                urgency_bonus = (due_time - job_completion_time[job]) * 0.01 if (due_time - job_completion_time[job]) > 0 else 0

                adjusted_start_time = start_time + load_penalty - urgency_bonus

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

        start_time = max(machine_available_time[best_machine], job_completion_time[best_job])
        end_time = start_time + best_time

        if best_job not in schedule:
            schedule[best_job] = []

        schedule[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[best_job] = end_time
        machine_load[best_machine] += best_time
        remaining_operations[best_job].pop(0)

    return schedule
