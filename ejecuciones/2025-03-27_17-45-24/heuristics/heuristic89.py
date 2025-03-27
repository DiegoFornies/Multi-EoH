
def heuristic(input_data):
    """FJSSP heuristic minimizing makespan with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    # Iterate through operations, prioritizing shortest processing time
    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            operations.append((job, op_idx, machines, times))

    # Sort by shortest processing time (estimated)
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')
        best_start_time = 0
        best_processing_time = 0

        # Find the machine that minimizes makespan, considering machine load
        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time
            load_factor = machine_load[machine]
            if end_time + 0.1*load_factor < min_end_time:
                min_end_time = end_time + 0.1*load_factor
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

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

    return schedule
