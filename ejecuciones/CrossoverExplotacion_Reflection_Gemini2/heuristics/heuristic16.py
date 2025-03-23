
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem that prioritizes minimizing idle time
    and balancing machine load using a shortest processing time on least loaded machine rule.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_assignments = {j: [] for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Initialize a list of operations that are ready to be scheduled
    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))  # (job_id, operation_index)

    while ready_operations:
        # Select the job-operation pair with the earliest possible start time
        best_job, best_op_index = None, None
        earliest_start_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]
            
            # Find the earliest possible start time for this operation
            min_start_time = float('inf')
            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                min_start_time = min(min_start_time, start_time)
                
            if min_start_time < earliest_start_time:
                earliest_start_time = min_start_time
                best_job, best_op_index = job_id, op_index

        job_id, op_index = best_job, best_op_index
        machines, times = jobs_data[job_id][op_index]
        
        # Select the machine with the shortest processing time that will also minimize idle time
        best_machine, best_processing_time = None, float('inf')
        earliest_completion_time = float('inf')
        
        for machine_id, processing_time in zip(machines, times):
            available_time = machine_available_times[machine_id]
            start_time = max(available_time, job_completion_times[job_id])
            completion_time = start_time + processing_time

            if completion_time < earliest_completion_time:
                earliest_completion_time = completion_time
                best_machine, best_processing_time = machine_id, processing_time

        # Schedule the operation on the selected machine
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Remove the scheduled operation from the ready operations list
        ready_operations.remove((job_id, op_index))

        # Add the next operation of the job to the ready operations list, if it exists
        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
