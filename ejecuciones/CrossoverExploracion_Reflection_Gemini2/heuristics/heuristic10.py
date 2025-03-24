
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes operations
    based on shortest processing time and earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    
    # Create a list of operations to schedule
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))  # (job, op_number, available_machines, processing_times)
    
    scheduled_operations = set() #Track scheduled operations, in tuple format (job, op_number)
    
    while len(scheduled_operations) < sum(len(ops) for ops in jobs_data.values()): #While all operations are not scheduled

        # Find the next operation to schedule
        eligible_operations = []
        for job, op_num, machines, times in operations:
            if (job, op_num) not in scheduled_operations:
                
                #Check operation sequence feasibility
                if op_num > 1: 
                    #If the operation is not the first one, ensure the previous one is already scheduled
                    prev_op_num = op_num - 1
                    if (job, prev_op_num) not in scheduled_operations:
                        continue #Skip this operation as the previous one is not scheduled

                eligible_operations.append((job, op_num, machines, times))
        
        if not eligible_operations:
            break # Break if no operations is available to schedule

        # Select best operation based on heuristic
        best_operation = None
        min_end_time = float('inf')

        for job, op_num, machines, times in eligible_operations:
            
            best_machine = None
            min_operation_end_time = float('inf')
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                if end_time < min_operation_end_time:
                    min_operation_end_time = end_time
                    best_machine = machine

            if min_operation_end_time < min_end_time:
                min_end_time = min_operation_end_time
                best_operation = (job, op_num, best_machine, min_end_time - machine_available_time[best_machine] - job_completion_time[job] + machine_available_time[best_machine] ) #job, op_num, machine, processing time

        # Schedule the best operation
        if best_operation:
            job, op_num, best_machine, processing_time = best_operation # processing_time = end_time - machine_available_time[best_machine] - job_completion_time[job] + machine_available_time[best_machine]
            start_time = max(machine_available_time[best_machine], job_completion_time[job]) #Check feasibility based on when either the machine or the job is available
            end_time = start_time + processing_time
            schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })
                
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time
            scheduled_operations.add((job, op_num))

    return schedule
