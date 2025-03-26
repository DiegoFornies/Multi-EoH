
def heuristic(input_data):
    """Prioritizes operations based on remaining work and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_operations_scheduled = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_work = {j: sum(min(t) for _, t in ops) for j, ops in jobs.items()}

    while any(job_operations_scheduled[j] < len(jobs[j]) for j in range(1, n_jobs + 1)):
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            op_idx = job_operations_scheduled[job]
            if op_idx < len(jobs[job]):
                eligible_operations.append((job, op_idx))

        def operation_priority(item):
            job, op_idx = item
            machines, times = jobs[job][op_idx]
            min_time = min(times)
            priority = remaining_work[job] + 0.1 * min_time
            return priority

        eligible_operations.sort(key=operation_priority)

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]
            op_num = op_idx + 1

            best_machine = None
            min_completion_time = float('inf')
            best_processing_time = None
            best_start_time = None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time
            job_operations_scheduled[job] += 1
            remaining_work[job] -= best_processing_time

    return schedule
