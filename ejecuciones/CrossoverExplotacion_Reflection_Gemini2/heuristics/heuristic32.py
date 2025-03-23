
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) 
    that prioritizes minimizing machine idle time and job waiting time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}  # Store schedule for each job
    machine_available_time = {m: 0 for m in range(n_machines)}  # Keep track of when each machine is available
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Keep track of when each job is completed till now

    # Iterate through each job and its operations
    for job_id, operations in jobs.items():
        schedule[job_id] = []
        
        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine that minimizes the waiting time for the job
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None
            
            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                
                # Calculate the earliest possible start time for this operation on this machine
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                # If this start time is better than the current best, update the best machine
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            # Assign the operation to the best machine found
            start_time = min_start_time
            end_time = start_time + best_processing_time
            
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            
            # Update the machine's availability time and the job's completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
