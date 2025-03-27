
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with fewer machine options
    and assigns to machines with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Track completion time for each job.

    # Create a list of operations with additional info: (job_id, op_idx, machines, times)
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx, machines, times))

    # Sort operations based on the number of possible machines (ascending order)
    operations.sort(key=lambda x: len(x[2]))

    for job_id, op_idx, machines, times in operations:
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            processing_time = times[m_idx]
            
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = earliest_start_time
        end_time = start_time + best_processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time #Update job completion time

    return schedule
