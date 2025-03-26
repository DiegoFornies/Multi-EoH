
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with shorter processing times and machines with earlier availability.
    Considers machine load balancing and job completion time simultaneously.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in jobs_data.keys()}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data.keys()}

    # Create a list of available operations, initially the first operation of each job
    available_operations = []
    for job, operations in jobs_data.items():
        available_operations.append({
            'job': job,
            'op_idx': 0,
            'machines': operations[0][0],
            'times': operations[0][1]
        })

    while available_operations:
        # Select the operation with the shortest processing time
        best_operation = None
        shortest_time = float('inf')
        best_machine = None

        for operation in available_operations:
            job = operation['job']
            machines = operation['machines']
            times = operation['times']

            # Find the machine with the earliest available time for this operation
            earliest_machine = None
            earliest_time = float('inf')
            
            for i, machine in enumerate(machines):
                available_at = max(machine_available_time[machine], job_completion_time[job])
                if available_at < earliest_time:
                    earliest_time = available_at
                    earliest_machine = machine
            
            if earliest_machine is not None:
                time_index = machines.index(earliest_machine)
                processing_time = times[time_index]

                if processing_time < shortest_time:
                    shortest_time = processing_time
                    best_operation = operation
                    best_machine = earliest_machine

        if best_operation is None:
            # Handle the case where no operation can be scheduled (should not happen with valid input)
            print("Warning: No operation could be scheduled. Check input data.")
            break
        
        job = best_operation['job']
        op_idx = best_operation['op_idx']
        machines = best_operation['machines']
        times = best_operation['times']

        machine = best_machine  # Use the selected machine with earliest availability
        time_index = machines.index(machine)
        processing_time = times[time_index]

        start_time = max(machine_available_time[machine], job_completion_time[job])
        end_time = start_time + processing_time
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_time[machine] = end_time
        job_completion_time[job] = end_time

        # Remove the scheduled operation from available operations
        available_operations.remove(best_operation)

        # Add the next operation of the job to available operations, if any
        next_op_idx = op_idx + 1
        if next_op_idx < len(jobs_data[job]):
            next_machines = jobs_data[job][next_op_idx][0]
            next_times = jobs_data[job][next_op_idx][1]
            available_operations.append({
                'job': job,
                'op_idx': next_op_idx,
                'machines': next_machines,
                'times': next_times
            })

    return schedule
