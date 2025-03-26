
def heuristic(input_data):
    """Prioritizes shortest remaining processing time (SRPT) across jobs, balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_time = {}  # Remaining processing time for each job.
    schedule = {}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        job_remaining_time[job] = sum(min(op[1]) for op in jobs[job])  # Sum of shortest processing times.

    completed_jobs = set()
    current_operations = {job: 0 for job in range(1, n_jobs + 1)}  # Track operation indices for each job
    
    time = 0
    while len(completed_jobs) < n_jobs:
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if job not in completed_jobs:
                op_index = current_operations[job]
                if op_index < len(jobs[job]):
                    eligible_operations.append((job, op_index))

        # Select job with shortest remaining processing time that has an available operation.
        if not eligible_operations:
            time += 1 # No operations can be scheduled, advance time.
            continue
        
        best_job = None
        best_operation_index = None
        min_remaining_time = float('inf')
        for job, op_index in eligible_operations:
            if job_remaining_time[job] < min_remaining_time:
                min_remaining_time = job_remaining_time[job]
                best_job = job
                best_operation_index = op_index
        
        machines, times = jobs[best_job][best_operation_index]
        
        # Choose the machine with earliest availability
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[best_job])
            end_time = start_time + processing_time
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        schedule[best_job].append({
            'Operation': best_operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[best_job] = best_start_time + best_processing_time
        job_remaining_time[best_job] -= min(times)
        current_operations[best_job] += 1

        if current_operations[best_job] == len(jobs[best_job]):
            completed_jobs.add(best_job)

    return schedule
