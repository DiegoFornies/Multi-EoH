
def heuristic(input_data):
    """FJSSP heuristic: Combines EFT and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_next_operation = {job: 0 for job in range(1, n_jobs + 1)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    scheduled_count = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_count < total_operations:
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if job_next_operation[job] < len(jobs[job]):
                eligible_operations.append(job)

        if not eligible_operations:
            break

        urgent_job = min(eligible_operations, key=lambda job: job_completion_time[job])
        op_index = job_next_operation[urgent_job]
        machines, times = jobs[urgent_job][op_index]

        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for machine, time in zip(machines, times):
            start_time = max(machine_available_time[machine], job_completion_time[urgent_job])
            finish_time = start_time + time

            if finish_time < best_start_time:
                best_machine = machine
                best_start_time = start_time
                best_processing_time = time

        # Load Balancing
        initial_start_time = best_start_time
        initial_machine = best_machine
        for machine, time in zip(machines, times):
            start_time = max(machine_available_time[machine], job_completion_time[urgent_job])
            finish_time = start_time + time
            if (machine_load[best_machine] > machine_load[machine]):
                best_machine = machine
                best_start_time = start_time
                best_processing_time = time

        operation = {
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        }
        schedule[urgent_job].append(operation)

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[urgent_job] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time
        job_next_operation[urgent_job] += 1
        scheduled_count += 1

    return schedule
