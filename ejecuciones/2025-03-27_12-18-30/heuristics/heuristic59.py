
def heuristic(input_data):
    """Balances machine load and minimizes job idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    remaining_operations = {}
    for job in range(1, n_jobs + 1):
        remaining_operations[job] = [(i + 1, op) for i, op in enumerate(jobs_data[job])]

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, ops in remaining_operations.items():
            if ops:
                eligible_operations.append((job, ops[0]))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        min_idle_time = float('inf')

        for job, (op_num, (machines, times)) in eligible_operations:
            for m_idx, m in enumerate(machines):
                time = times[m_idx]
                start_time = max(machine_load[m], job_completion_time[job])
                idle_time = start_time - job_completion_time[job] if start_time > job_completion_time[job] else 0

                if idle_time < min_idle_time:
                    min_idle_time = idle_time
                    best_operation = (job, (op_num, (machines, times)))
                    best_machine = m

        if best_operation is not None and best_machine is not None:
            job, (op_num, (machines, times)) = best_operation
            m_idx = machines.index(best_machine)
            processing_time = times[m_idx]
            start_time = max(machine_load[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_load[best_machine] = end_time
            job_completion_time[job] = end_time
            remaining_operations[job].pop(0)

    return schedule
