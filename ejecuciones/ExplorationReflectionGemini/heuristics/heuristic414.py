
def heuristic(input_data):
    """Prioritizes critical operations and balances machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_operations_scheduled = {job: 0 for job in jobs}

    def calculate_priority(job, op_index):
        machines, times = jobs[job][op_index]
        min_time = min(times)
        # Simple heuristic: shorter processing time, higher priority
        return 1 / (min_time + 0.001)  # Avoid division by zero

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        eligible_operations = []
        for job in jobs:
            op_index = job_operations_scheduled[job]
            if op_index < len(jobs[job]):
                eligible_operations.append((job, op_index))

        eligible_operations.sort(key=lambda x: calculate_priority(x[0], x[1]), reverse=True)

        for job, op_index in eligible_operations:
            machines, times = jobs[job][op_index]
            op_num = op_index + 1

            best_machine, best_start_time, processing_time = None, float('inf'), None
            min_cost = float('inf')

            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job], machine_available_times[m])
                end_time = start_time + times[i]
                future_load = machine_load[m] + times[i]
                # Adjusted cost function: prioritize load balancing
                cost = times[i] + 0.5 * future_load + 0.001 * start_time

                if cost < min_cost:
                    min_cost = cost
                    best_machine = m
                    best_start_time = start_time
                    processing_time = times[i]

            if best_machine is not None:
                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': best_start_time,
                    'End Time': best_start_time + processing_time,
                    'Processing Time': processing_time
                })

                machine_load[best_machine] += processing_time
                machine_available_times[best_machine] = best_start_time + processing_time
                job_completion_times[job] = best_start_time + processing_time
                job_operations_scheduled[job] += 1

    return schedule
