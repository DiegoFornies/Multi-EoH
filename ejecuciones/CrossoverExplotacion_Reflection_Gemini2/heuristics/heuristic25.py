
def heuristic(input_data):
    """Schedules jobs using a greedy heuristic considering earliest available machine and shortest processing time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations and shuffle to encourage diversity
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))
    
    #Sort operations to schedule the shortest processing operations first
    operations.sort(key=lambda x: min(x[3]))

    # Iterate through operations
    while operations:
        best_op, best_machine, best_start_time, best_processing_time = None, None, float('inf'), None
        
        #Try multiple times
        for _ in range(len(operations)):
            job_id, op_num, machines, times = operations.pop(0)
            
            # Find the earliest available time for each machine that can perform the operation
            earliest_start_times = {}
            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                available_time = machine_available_times[machine]
                start_time = max(available_time, job_completion_times[job_id])
                earliest_start_times[machine] = (start_time, processing_time)
            
            # Find the machine with the earliest start time
            if earliest_start_times:
                machine = min(earliest_start_times, key=lambda k: earliest_start_times[k][0])
                start_time, processing_time = earliest_start_times[machine]
                
                # Update best if better or the first one checked
                if best_start_time > start_time :
                    best_op = (job_id, op_num, machines, times)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
                else:
                    operations.append((job_id, op_num, machines, times))
            else:
                operations.append((job_id, op_num, machines, times))

        # No feasible schedule found
        if best_op is None:
            break
        
        job_id, op_num, machines, times = best_op
        # Update the schedule
        start_time = best_start_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
