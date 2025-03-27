
def heuristic(input_data):
    """A heuristic for FJSSP minimizing makespan and balancing load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx, machines, times))

    # Sort operations based on shortest processing time on available machine.
    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_idx, machines, times in operations:
        min_end_time = float('inf')
        best_machine = None
        best_processing_time = None
        start_time = None

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            available_time = machine_available_time[machine]
            job_ready_time = job_completion_time[job_id]

            start = max(available_time, job_ready_time)
            end = start + processing_time

            if end < min_end_time:
                min_end_time = end
                best_machine = machine
                best_processing_time = processing_time
                start_time = start

        end_time = start_time + best_processing_time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        machine_load[best_machine] += best_processing_time

    return schedule
