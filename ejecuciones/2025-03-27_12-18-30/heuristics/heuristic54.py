
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job_id: [] for job_id in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Prioritize operations based on shortest processing time
    operation_priority = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            min_time = min(times)
            operation_priority.append((min_time, job_id, op_idx))

    operation_priority.sort()  # Sort by shortest processing time

    for _, job_id, op_idx in operation_priority:
        operation = jobs[job_id][op_idx]
        machines, times = operation
        
        # Chooses the machine that allows the earliest end time
        best_machine = None
        earliest_end_time = float('inf')
        
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time
            
            if end_time < earliest_end_time:
                earliest_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
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

    return schedule
