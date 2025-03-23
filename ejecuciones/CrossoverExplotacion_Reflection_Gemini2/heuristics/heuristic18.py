
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules operations greedily based on shortest processing time, 
    prioritizing jobs with fewer remaining operations. Minimizes makespan and balances
    machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    remaining_operations = {job: len(jobs_data[job]) for job in range(1, n_jobs + 1)}
    
    eligible_operations = []
    for job in range(1, n_jobs + 1):
        if remaining_operations[job] > 0:
            eligible_operations.append((job, 1)) # (job_id, operation_number)
    
    while eligible_operations:
        # Prioritize jobs with the fewest remaining operations
        eligible_operations.sort(key=lambda x: remaining_operations[x[0]])

        job_id, operation_number = eligible_operations.pop(0)
        
        # Get operation data
        operation_index = operation_number - 1 # Index starts from 0
        machines, times = jobs_data[job_id][operation_index]
        
        # Find the machine with the earliest available time that can process this operation
        best_machine = None
        min_end_time = float('inf')
        
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine+1], job_completion_time[job_id])
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine + 1 # Machines are 1-indexed

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        processing_time = times[machines.index(best_machine-1)]
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        
        # Update remaining operations
        remaining_operations[job_id] -= 1
        
        # Add the next operation of the job to the eligible operations list, if it exists
        next_operation_number = operation_number + 1
        if next_operation_number <= len(jobs_data[job_id]):
            eligible_operations.append((job_id, next_operation_number))
    
    return schedule
