
def heuristic(input_data):
    """
    Heuristic scheduling algorithm for FJSSP minimizing makespan by considering machine load and job progress.
    Prioritizes operations based on remaining processing time of the job.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}
    job_remaining_time = {}

    # Calculate initial remaining processing time for each job
    for job, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)  # optimistic, take min processing time if several options.
        job_remaining_time[job] = total_time

    # Create a list of operations ready to be scheduled
    ready_operations = []
    for job, operations in jobs.items():
        ready_operations.append((job, 0))  # (job_id, operation_index)

    while ready_operations:
        # Prioritize operations from jobs with less remaining processing time
        ready_operations.sort(key=lambda x: job_remaining_time[x[0]])

        job_id, op_idx = ready_operations.pop(0)
        machines, times = jobs[job_id][op_idx]
        
        # Find the best machine for the operation (earliest finish time)
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx, m in enumerate(machines):
          start_time = max(machine_available_time[m], job_completion_time[job_id])
          processing_time = times[m_idx]
          if start_time + processing_time < best_start_time:
                best_machine, best_start_time, best_processing_time = m, start_time, processing_time
        
        # Schedule the operation on the best machine
        machine = best_machine
        start_time = best_start_time
        processing_time = best_processing_time
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        op_num = op_idx + 1
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine available time and job completion time
        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        job_remaining_time[job_id] -= processing_time  # Update the remaining time

        # Add the next operation of the job to the ready list (if it exists)
        next_op_idx = op_idx + 1
        if next_op_idx < len(jobs[job_id]):
            ready_operations.append((job_id, next_op_idx))

    return schedule
