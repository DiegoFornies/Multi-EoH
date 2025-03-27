
def heuristic(input_data):
    """A heuristic for FJSSP scheduling that considers machine load and operation processing times."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine availability
    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort operations by shortest processing time
    operation_priority = []
    for job, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            min_time = min(times)
            operation_priority.append((min_time, job, op_idx))

    operation_priority.sort()

    # Schedule operations
    for _, job, op_idx in operation_priority:
        machines, times = jobs[job][op_idx]

        # Find the earliest available machine for the operation, considering job sequence
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for m_idx, m in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_availability[m], job_completion_times[job])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = processing_time
        
        # Update schedule
        end_time = best_start_time + best_processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job availability
        machine_availability[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
