
def heuristic(input_data):
    """Schedules jobs prioritizing machine utilization and job order."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Prioritize machine utilization
        best_operation = None
        best_utilization = -1

        for job, op_num, machines, times in eligible_operations:
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])
                utilization = 1 / (machine_available_time[m] + 1) # Avoid divide by zero

                if utilization > best_utilization:
                    best_utilization = utilization
                    best_operation = (job, op_num, m, start_time, times[m_idx])

        if best_operation:
            job, op_num, machine, start_time, processing_time = best_operation

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = start_time + processing_time
            job_completion_time[job] = start_time + processing_time

            remaining_operations[job].pop(0)

    return schedule
