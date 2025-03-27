
def heuristic(input_data):
    """Heuristic for FJSSP using a global makespan estimation."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Calculate total processing time for each job to estimate makespan contribution
    job_processing_times = {}
    for job_id in range(1, n_jobs + 1):
      job_processing_times[job_id] = sum(min(op[1]) for op in jobs[job_id])

    # Sort jobs by their total processing time in descending order
    job_order = sorted(job_processing_times, key=job_processing_times.get, reverse=True)

    for job_id in job_order:
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_index, operation in enumerate(operations):
            eligible_machines = operation[0]
            processing_times = operation[1]

            # Choose machine that minimizes the operation's end time
            best_machine = None
            min_end_time = float('inf')
            best_processing_time = 0

            for machine_index, machine_id in enumerate(eligible_machines):
                processing_time = processing_times[machine_index]
                start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id
                    best_processing_time = processing_time

            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
