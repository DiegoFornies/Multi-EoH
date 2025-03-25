
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes operations based on shortest processing time first (SPT)
    and selects the machine with the earliest available time for each operation to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

    # Create a list of all operations with their job and operation number.
    operations = []
    for job, operations_list in jobs.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job, op_idx + 1, machines, times))
    
    #Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        # Find the earliest available machine and time for the current operation.
        best_machine = None
        min_start_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_time = times[i]

        # Schedule the operation on the selected machine.
        start_time = min_start_time
        end_time = start_time + best_time
        processing_time = best_time
        
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': processing_time})

        # Update the machine's available time and the job's completion time.
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
    
    return schedule
