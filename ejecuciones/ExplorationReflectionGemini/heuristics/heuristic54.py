
def heuristic(input_data):
    """Improves balance by delaying job starts."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Introduce a delay to balance the load.
    initial_delay = 5

    for job in jobs:
        schedule[job] = []
        delay = initial_delay * job  # Vary the delay based on job ID
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                available_time = machine_available_time[machine]
                job_ready_time = job_completion_time[job] + delay # Apply delay
                start_time = max(available_time, job_ready_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            if best_machine is not None:
                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': best_start_time,
                    'End Time': best_start_time + best_processing_time,
                    'Processing Time': best_processing_time
                })

                machine_available_time[best_machine] = best_start_time + best_processing_time
                job_completion_time[job] = best_start_time + best_processing_time

    return schedule
