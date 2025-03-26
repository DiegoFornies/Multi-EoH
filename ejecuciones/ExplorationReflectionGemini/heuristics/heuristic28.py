
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time by 
    assigning operations to the machine that becomes available earliest.
    """
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_loads = {m: 0 for m in range(n_machines)}
    job_completion_times = {job_id: 0 for job_id in jobs}
    schedule = {}

    for job_id in jobs:
        schedule[job_id] = []
        
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations by job ID to maintain job sequence
    operations.sort(key=lambda x: x[0]) 

    while operations:
        best_op = None
        best_machine = None
        earliest_start = float('inf')
        
        # Find the operation from the job that's ready for execution
        for idx, (job_id, op_num, machines, times) in enumerate(operations):
            last_op_end_time = job_completion_times[job_id]
            
            # Check machine options and find the best
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]

                # Calculate potential start time
                start_time = max(machine_available_times[machine], last_op_end_time)
                
                # Pick the earliest possible start time
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = idx
                    best_machine = machine
                    best_processing_time = processing_time

        # Schedule the operation
        job_id, op_num, machines, times = operations.pop(best_op)
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time
        
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine and job times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_loads[best_machine] += best_processing_time

    return schedule
