
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    It prioritizes operations based on shortest processing time (SPT)
    among available machines, aiming to minimize makespan and idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Corrected job indexing
    
    # Create a list of all operations to schedule
    operations = []
    for job_id, job_operations in jobs_data.items():
        for op_idx, op_data in enumerate(job_operations):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': op_data[0],
                'times': op_data[1]
            })
    
    # Sort operations based on shortest processing time on available machines
    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        # Find the machine with the earliest available time for this operation
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])  # Corrected job_id
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        start_time = min_start_time
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

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time # Corrected job_id

    return schedule
