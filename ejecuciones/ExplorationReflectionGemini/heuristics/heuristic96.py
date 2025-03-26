
def heuristic(input_data):
    """FJSSP heuristic: Priority dispatching rule based on total work remaining."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Calculate total work remaining for each job
    job_remaining_work = {}
    for job in range(1, n_jobs + 1):
        total_work = 0
        for operation in jobs[job]:
            total_work += min(operation[1])  # Estimate work by shortest time
        job_remaining_work[job] = total_work

    # Create a list of operations
    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job]):
            operations.append((job, op_idx + 1, operation))

    while operations:
        # Find eligible operations (previous operations are completed and have not been scheduled yet)
        eligible_operations = []
        for job, op_num, operation in operations:
            if op_num == 1 or schedule[job][-1]['Operation'] == op_num - 1 if job in schedule else True:
                eligible_operations.append((job, op_num, operation))
        
        # Prioritize operations based on remaining work
        eligible_operations.sort(key=lambda x: job_remaining_work[x[0]], reverse=True) #sort jobs for priority

        job, op_num, operation = eligible_operations[0]
        machines, times = operation

        # Find best machine with earliest completion
        best_machine = None
        min_completion_time = float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            available_time = machine_available_time[machine]
            job_ready_time = job_completion_time[job] if job in job_completion_time else 0 # handle uncompleted jobs
            start_time = max(available_time, job_ready_time)
            completion_time = start_time + processing_time

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Schedule the operation
        if job not in schedule:
             schedule[job] = [] # Create schedule list if not there
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job times
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time
        
        # Update remaining work
        job_remaining_work[job] -= best_processing_time

        # Remove scheduled operation
        operations.remove((job, op_num, operation))
            
    return schedule
