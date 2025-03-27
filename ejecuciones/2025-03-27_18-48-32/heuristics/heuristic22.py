
def heuristic(input_data):
    """A simple heuristic for FJSSP: Assigns each operation to the earliest available machine, minimizing idle time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}  # Store the final schedule
    machine_available_times = {m: 0 for m in range(n_machines)}  # Track when each machine is available
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}  # Track when each job's previous operation is complete

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, operation in enumerate(operations):
            eligible_machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for m_idx, machine_id in enumerate(eligible_machines):
                processing_time = processing_times[m_idx]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine_id
                    best_processing_time = processing_time

            start_time = min_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
