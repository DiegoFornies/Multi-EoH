
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes jobs with fewer remaining operations and
    assigns operations to machines with the earliest available time, considering
    machine load balancing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule and machine availability
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_availability = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    remaining_operations = {job: list(range(1, len(jobs_data[job]) + 1)) for job in range(1, n_jobs + 1)}
    
    # Initialize a list of runnable operations with job and operation numbers
    runnable_operations = []
    for job in range(1, n_jobs + 1):
        if remaining_operations[job]:
            runnable_operations.append((job, remaining_operations[job][0]))
    
    while runnable_operations:
        # Prioritize jobs with fewer remaining operations
        runnable_operations.sort(key=lambda x: len(remaining_operations[x[0]]))

        job_number, operation_number = runnable_operations.pop(0)
        operation_index = operation_number - 1
        machines, times = jobs_data[job_number][operation_index]

        # Find the machine with the earliest available time and minimum estimated load
        best_machine, best_time, min_load = None, float('inf'), float('inf')
        for i, machine in enumerate(machines):
            available_time = max(machine_availability[machine], job_completion_times[job_number])
            load = 0
            #Estimate load on machine by summing all operations to be processed
            for job_i in range(1, n_jobs + 1):
                 for op_idx in range(len(jobs_data[job_i])):
                     machines_j, times_j = jobs_data[job_i][op_idx]
                     if machine in machines_j:
                         load+= times_j[machines_j.index(machine)]

            if available_time < best_time or (available_time == best_time and load < min_load):
                best_machine = machine
                best_time = available_time
                min_load = load


        processing_time = times[machines.index(best_machine)]
        start_time = max(machine_availability[best_machine], job_completion_times[job_number])
        end_time = start_time + processing_time
        
        schedule[job_number].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        # Update machine availability and job completion time
        machine_availability[best_machine] = end_time
        job_completion_times[job_number] = end_time
        
        # Remove the completed operation and add the next operation
        remaining_operations[job_number].pop(0)
        if remaining_operations[job_number]:
            runnable_operations.append((job_number, remaining_operations[job_number][0]))

    return schedule
