
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem that aims to minimize makespan
    by prioritizing operations with the shortest processing time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations, with job and operation indices
    all_operations = []
    for job_id, operations in jobs.items():
        for op_idx, operation in enumerate(operations):
            all_operations.append((job_id, op_idx + 1, operation))

    # Sort operations by shortest processing time
    all_operations.sort(key=lambda x: min(x[2][1]))  # Sort by minimum processing time

    for job_id, op_num, operation in all_operations:
        machines, times = operation
        
        # Find the earliest available machine for this operation
        best_machine = None
        min_start_time = float('inf')

        for machine_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_time = times[machine_idx]
                best_machine_idx = machine_idx
            
        # schedule the operation on the best available machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        
    return schedule
