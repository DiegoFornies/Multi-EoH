
def heuristic(input_data):
    """FJSSP heuristic: Balances makespan, load using dynamic priorities."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_next_operation = {job: 0 for job in range(1, n_jobs + 1)}

    scheduled_count = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())

    while scheduled_count < total_operations:
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if job_next_operation[job] < len(jobs_data[job]):
                eligible_operations.append(job)

        if not eligible_operations:
            break

        urgent_job = min(eligible_operations, key=lambda job: job_completion_time[job])
        op_index = job_next_operation[urgent_job]
        machines, times = jobs_data[urgent_job][op_index]

        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for machine_index, machine in enumerate(machines):
            time = times[machine_index]
            start_time = max(machine_available_time[machine], job_completion_time[urgent_job])
            end_time = start_time + time

            load_factor = machine_load[machine]
            # Dynamic weight: Prefer load balancing early, makespan later
            weight = 0.1 if scheduled_count < total_operations / 2 else 0.01
            score = end_time + weight * load_factor

            if score < best_start_time + weight * (machine_load[best_machine] if best_machine is not None else 0):
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
