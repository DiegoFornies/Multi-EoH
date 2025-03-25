
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes operations based on the shortest processing time among available machines and minimizes idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    # Operations that are available to be scheduled
    available_operations = {}
    for job in jobs:
        available_operations[job] = 0 # index of the first operation

    # Initialize the schedule
    for job in jobs:
        schedule[job] = []

    scheduled_operations = 0
    total_operations = sum(len(job_ops) for job_ops in jobs.values())

    while scheduled_operations < total_operations:
        # Find the best operation to schedule
        best_operation = None
        best_job = None
        earliest_start_time = float('inf')
        
        for job in jobs:
            op_idx = available_operations[job]
            if op_idx < len(jobs[job]):
                machines, times = jobs[job][op_idx]
                
                # Find the machine that allows the earliest start time
                for i in range(len(machines)):
                    machine = machines[i]
                    processing_time = times[i]
                    
                    start_time = max(machine_available_time[machine], job_completion_time[job])
                    
                    if start_time < earliest_start_time:
                        earliest_start_time = start_time
                        best_operation = (machine, processing_time, op_idx)
                        best_job = job

        # Schedule the best operation
        if best_operation is not None:
            machine, processing_time, op_idx = best_operation
            job = best_job

            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time
                
            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_available_time[machine] = end_time
            job_completion_time[job] = end_time

            # Advance to the next operation for the job
            available_operations[job] += 1
            scheduled_operations += 1
        else:
            # If no operation can be scheduled, advance machine time
            min_machine_time = min(machine_available_time.values())
            for m in machine_available_time:
                machine_available_time[m] = max(machine_available_time[m], min_machine_time + 1)

    return schedule
