
def heuristic(input_data):
    """Heuristic for FJSSP: Prioritize operations with shortest processing time
       and earliest machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations, each operation is a tuple:
    # (job_id, operation_index, list of available machines, list of processing times)
    operations = []
    for job_id, job_data in jobs.items():
        for op_index, op_data in enumerate(job_data):
            operations.append((job_id, op_index, op_data[0], op_data[1]))
    
    # Sort operations by shortest processing time first.
    operations.sort(key=lambda op: min(op[3]))
    
    # Schedule operations
    for job_id, op_index, available_machines, processing_times in operations:
        best_machine = -1
        min_end_time = float('inf')
        best_processing_time = -1

        for i, machine in enumerate(available_machines):
            processing_time = processing_times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time

        # Assign operation to the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []
        
        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        
    return schedule
