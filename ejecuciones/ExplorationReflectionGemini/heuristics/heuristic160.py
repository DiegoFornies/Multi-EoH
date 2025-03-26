
def heuristic(input_data):
    """
    Schedules jobs considering shortest processing time, machine availability, and load balancing.
    Dynamically balances SPT and load balancing based on machine availability.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}  # Keep track of machine load
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        best_start_time = float('inf')
        best_processing_time = float('inf')
        best_machine_load = float('inf')  # Initialize best_machine_load

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the earliest possible start time for this operation and machine
            earliest_start_time = float('inf')  # Fix initialization
            selected_machine = None
            selected_time = None

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])

                if start_time < earliest_start_time:  # Check < not >
                    earliest_start_time = start_time
                    selected_machine = machine
                    selected_time = time

            processing_time = selected_time

            # Calculate machine load after assigning the operation
            hypothetical_load = machine_load[selected_machine] + processing_time

            # Dynamically adjust weights based on machine availability.
            # If machines are heavily loaded, prioritize shortest processing time.
            # Otherwise, balance the load.
            availability_factor = max(0, 1 - (machine_available_times[selected_machine] / sum(machine_available_times.values(),1e-9))) #Avoid zero division

            #Heuristic score combine earliest_start_time, processing_time, load
            heuristic_score = (earliest_start_time * 0.4 +
                                processing_time * 0.3 +
                                hypothetical_load * availability_factor * 0.3)

            #Prioritize the lower heuristic_score
            if best_op is None or heuristic_score < (best_start_time * 0.4 + best_processing_time * 0.3 + best_machine_load * 0.3):
                best_start_time = earliest_start_time
                best_processing_time = processing_time
                best_op = op_data
                best_machine = selected_machine
                best_time = selected_time
                best_machine_load = hypothetical_load


        # Schedule the best operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine availability, job completion time, and machine load
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[best_machine] += best_time

        # Remove the scheduled operation from available operations and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
