
def heuristic(input_data):
    """Schedules jobs by prioritizing operations with fewer machine options and minimizing idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times

    # Flatten operations into a list with job information for sorting
    flattened_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            flattened_operations.append((len(machines), job_id, op_idx, machines, times))

    # Sort operations by the number of available machines (least first)
    flattened_operations.sort(key=lambda x: x[0])

    for _, job_id, op_idx, machines, times in flattened_operations:
        op_num = op_idx + 1
        
        # Find the best machine to minimize idle time
        best_machine, best_time = None, float('inf')
        for i, machine in enumerate(machines):
            available_time = machine_available_time[machine]
            job_time = job_completion_time[job_id]
            start_time = max(available_time, job_time)
            
            if start_time < best_time:
                best_machine = machine
                best_time = start_time

        processing_time = times[machines.index(best_machine)] #find the correct processing time
        start_time = best_time
        end_time = start_time + processing_time
        
        # Update schedule
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
