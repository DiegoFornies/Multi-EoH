
def heuristic(input_data):
    """
    Heuristic for FJSSP using shortest processing time and earliest machine availability.
    Prioritizes operations with shorter processing times and assigns them to the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Flatten the jobs into a list of operations with job and operation number
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op_data))  # (job_id, operation_number, operation_data)
    
    # Sort operations based on shortest processing time
    operations.sort(key=lambda x: min(x[2][1]))  # Sort by min processing time

    for job_id, op_num, op_data in operations:
        machines, times = op_data

        # Find the machine with earliest available time that can perform the operation
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_time = times[i]
                best_start = start_time


        # Schedule the operation on the best machine
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start,
            'End Time': best_start + best_time,
            'Processing Time': best_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = best_start + best_time
        job_completion_time[job_id] = best_start + best_time

    return schedule
