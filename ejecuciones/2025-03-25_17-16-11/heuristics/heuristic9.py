
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes jobs with shorter total processing times.
    Assigns operations to the earliest available machine among feasible options.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Calculate total processing time for each job
    job_processing_times = {}
    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_processing_times[job] = total_time

    # Sort jobs by total processing time (shortest first)
    sorted_jobs = sorted(job_processing_times.keys(), key=job_processing_times.get)

    # Initialize schedule and machine availability
    schedule = {job: [] for job in jobs_data}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}

    for job in sorted_jobs:
        operations = jobs_data[job]
        for op_idx, (machines, times) in enumerate(operations):
            op_num = op_idx + 1
            best_machine, best_start_time = None, float('inf')
            
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_availability[machine], job_completion_times[job])
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = times[m_idx]

            start_time = best_start_time
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_availability[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
