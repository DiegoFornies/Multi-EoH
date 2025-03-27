
def heuristic(input_data):
    """Schedules jobs balancing load and urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
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

            # Prioritize machines with lower current load.
            machine_loads = {m: machine_available_times[m] for m in machines}
            sorted_machines = sorted(machine_loads, key=machine_loads.get)

            # Check the priority for the sorting
            for m in sorted_machines:
                m_idx = machines.index(m)
                start_time = max(machine_available_times[m], job_completion_times[job])

                # Urgency: Prioritize jobs with shorter remaining operations.
                remaining_time = 0
                for future_op_num in range(op_num, len(jobs_data[job]) + 1):
                    if future_op_num <= len(jobs_data[job]):
                        future_machines, future_times = jobs_data[job][future_op_num - 1]
                        min_future_time = min(future_times)
                        remaining_time += min_future_time

                # Introduce a simple urgency factor.
                start_time -= remaining_time * 0.01  # Small boost for urgent jobs

                if start_time < earliest_start:
                    earliest_start = start_time
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
