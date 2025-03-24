
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes shortest processing time and earliest machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []

    # Create a list of operations, sorted by shortest processing time first (SPT).
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))  # (job, op_num, machines, times)

    # Sort operations by minimum processing time among available machines
    operations.sort(key=lambda op: min(op[3]))
    
    for job, op_num, machines, times in operations:
        # Find the earliest available machine for the operation.
        best_machine = -1
        earliest_start_time = float('inf')
        best_processing_time = float('inf') # Tie breaker - minimize processing time
        
        for i, machine in enumerate(machines):
            start_time = max(machine_available_times[machine], job_completion_times[job])
            processing_time = times[i]

            if start_time < earliest_start_time or (start_time == earliest_start_time and processing_time < best_processing_time):
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time
        
        # Schedule the operation on the best machine.
        start_time = earliest_start_time
        processing_time = best_processing_time
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time.
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time
    
    return schedule
