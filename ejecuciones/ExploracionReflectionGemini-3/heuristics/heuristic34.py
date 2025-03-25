
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes operations based on shortest processing time, 
    considers machine availability, and attempts to minimize idle time within jobs.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations with their job and operation numbers
    all_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations by shortest processing time first
    all_operations.sort(key=lambda x: min(x[3])) # Sort by shortest processing time.

    for job_id, op_num, machines, times in all_operations:
        # Find the best machine for the current operation
        best_machine = -1
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_last_end_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        if job_id not in schedule:
            schedule[job_id] = []
        
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_last_end_time[job_id] = best_start_time + best_processing_time

    return schedule
