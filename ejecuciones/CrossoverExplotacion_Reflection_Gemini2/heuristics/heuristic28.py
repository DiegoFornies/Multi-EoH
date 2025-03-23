
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes operations with the shortest processing time
    and assigns them to the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs_data}

    operations = []
    for job_id, job in jobs_data.items():
        for op_id, operation in enumerate(job):
            operations.append((job_id, op_id, operation))

    # Sort operations by shortest processing time available
    operations.sort(key=lambda x: min(x[2][1]))

    for job_id, op_id, operation in operations:
        machines, times = operation
        best_machine, best_time, start_time = None, float('inf'), None
        
        # Find the earliest available time on feasible machines
        for i, machine in enumerate(machines):
            available_time = max(machine_available_times[machine], job_completion_times[job_id])
            if times[i] < best_time or (times[i] == best_time and available_time < start_time):
                best_machine, best_time, start_time = machine, times[i], available_time

        # Assign the operation to the selected machine
        end_time = start_time + best_time
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_id + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine availability and job completion time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
