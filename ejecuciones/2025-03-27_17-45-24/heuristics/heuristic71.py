
def heuristic(input_data):
    """Combines makespan, load balance, and job progress for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {job: list(range(len(ops))) for job, ops in jobs_data.items()}

    while any(remaining_operations[job] for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if remaining_operations[job]:
                eligible_operations.append((job, remaining_operations[job][0]))

        best_operation = None
        best_machine = None
        min_weighted_end_time = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs_data[job][op_idx]
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time
                load_factor = machine_load[machine]
                weighted_end_time = end_time + 0.1 * load_factor  # Balance makespan and load
                if weighted_end_time < min_weighted_end_time:
                    min_weighted_end_time = weighted_end_time
                    best_operation = (job, op_idx)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        if best_operation is not None:
            job, op_idx = best_operation

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
            remaining_operations[job].pop(0)

    return schedule
