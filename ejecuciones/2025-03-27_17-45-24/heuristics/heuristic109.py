
def heuristic(input_data):
    """FJSSP heuristic: Hybrid approach - SPT-based job selection + load-aware machine selection."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    completed_operations = {job: 0 for job in range(1, n_jobs + 1)}

    while any(completed_operations[job] < len(jobs_data[job]) for job in range(1, n_jobs + 1)):
        eligible_jobs = [job for job in range(1, n_jobs + 1) if completed_operations[job] < len(jobs_data[job])]

        # SPT-based job selection: Select the job with the shortest processing time for its next operation.
        job = min(eligible_jobs, key=lambda j: min(jobs_data[j][completed_operations[j]][1]))

        op_idx = completed_operations[job]
        machines, times = jobs_data[job][op_idx]

        # Load-aware machine selection: Select the machine with the lowest load that can perform the operation.
        best_machine = None
        min_end_time = float('inf')
        best_start_time = 0
        best_processing_time = 0

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            # Prioritize less loaded machines using a scaled load factor
            load_factor = machine_load[machine] / (sum(machine_load.values()) + 1e-9) if sum(machine_load.values()) > 0 else 0
            if end_time + 0.1*load_factor < min_end_time:
                min_end_time = end_time + 0.1*load_factor
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        schedule[job] = schedule.get(job, [])
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time
        completed_operations[job] += 1

    return schedule
