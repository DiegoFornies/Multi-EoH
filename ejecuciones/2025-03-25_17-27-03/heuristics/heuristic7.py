
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes operations with the fewest machine choices and shortest processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    # Maintain a list of operations ready to be scheduled for each job
    ready_operations = {job_id: 0 for job_id in jobs}
    
    # Maintain a list of unscheduled operations as tuples (job_id, op_index)
    unscheduled_operations = []
    for job_id, operations in jobs.items():
        unscheduled_operations.append((job_id, 0)) # start with first operation
    
    while unscheduled_operations:
        # Filter unscheduled operations to those that are ready (all preceeding ops done)
        available_operations = []
        for job_id, op_index in unscheduled_operations:
            is_ready = True
            if op_index > 0:
                # Check that previous operation is complete
                if job_completion_time[job_id] < schedule[job_id][-1]['End Time']:
                    is_ready = False
            if is_ready:
                available_operations.append((job_id, op_index))
        
        if not available_operations:
            # no ready operations, break to avoid infinite loops
            break

        # Prioritize operations: fewest machine choices, then shortest processing time
        best_op = None
        min_machines = float('inf')
        min_time = float('inf')

        for job_id, op_index in available_operations:
            machines, times = jobs[job_id][op_index]
            
            if len(machines) < min_machines:
                min_machines = len(machines)
                min_time = min(times) # shortest time on any of the available machines
                best_op = (job_id, op_index)
            elif len(machines) == min_machines:
                if min(times) < min_time:
                    min_time = min(times)
                    best_op = (job_id, op_index)
        
        job_id, op_index = best_op
        machines, times = jobs[job_id][op_index]

        # Find the machine and time that minimizes completion time
        best_machine = None
        min_completion_time = float('inf')
        best_processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            completion_time = start_time + processing_time
            
            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time
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

        # Remove scheduled operation and add the next to unscheduled operations
        unscheduled_operations.remove((job_id, op_index))
        if op_index + 1 < len(jobs[job_id]):
            unscheduled_operations.append((job_id, op_index + 1))
        
    return schedule
