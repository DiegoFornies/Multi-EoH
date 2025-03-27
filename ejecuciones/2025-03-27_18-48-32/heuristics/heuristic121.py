
def heuristic(input_data):
    """Combines EDD and machine load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Prioritize operations based on combined criteria
        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_num, machines, times in eligible_operations:
            best_local_machine = None
            best_local_start = float('inf')
            best_local_time = None

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])
                load_penalty = machine_load[m] * 0.05 # Adjust as needed
                adjusted_start_time = start_time + load_penalty

                if adjusted_start_time < best_local_start:
                    best_local_start = adjusted_start_time
                    best_local_machine = m
                    best_local_time = times[m_idx]

            if best_local_start < earliest_start:
                earliest_start = best_local_start
                best_op = op_num
                best_machine = best_local_machine
                best_time = best_local_time
                best_job = job

        start_time = max(machine_available_time[best_machine], job_completion_time[best_job])

        if best_job not in schedule:
            schedule[best_job] = []

        schedule[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': start_time + best_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = start_time + best_time
        job_completion_time[best_job] = start_time + best_time
        machine_load[best_machine] += best_time

        remaining_operations[best_job].pop(0)

    return schedule
