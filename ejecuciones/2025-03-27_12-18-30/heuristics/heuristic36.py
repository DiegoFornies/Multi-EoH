
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing machine load using a shortest processing time (SPT) approach with machine load awareness."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs.keys()}

    # Flatten operations into a list of (job, op_idx, machines, times)
    flattened_ops = []
    for job, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            flattened_ops.append((job, op_idx, machines, times))
            
    # Sort operations by shortest processing time first.
    flattened_ops.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in flattened_ops:
        op_num = op_idx + 1
        
        # Find the machine with the earliest available time and lowest load.
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        
        for m_idx, m in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[m], job_completion_time[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = processing_time
            elif start_time == best_start_time and machine_load[m] < machine_load.get(best_machine,float('inf')):
                best_machine = m
                best_processing_time = processing_time

        # Schedule the operation on the best machine.
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time

        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times and load.
        machine_available_time[best_machine] = end_time
        machine_load[best_machine] = machine_load.get(best_machine,0) + best_processing_time
        job_completion_time[job] = end_time

    return schedule
