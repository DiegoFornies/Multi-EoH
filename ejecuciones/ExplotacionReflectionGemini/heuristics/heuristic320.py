
def heuristic(input_data):
    """A heuristic for FJSSP that adaptively balances makespan and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)} #track load to balance

    # Initialize schedule
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # Iterate through jobs and operations, scheduling greedily
    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))  # (job_id, operation_index)

    while available_operations:
        best_operation = None
        best_machine = None
        best_priority = float('inf') # Lower is better

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                #Adaptive Priority
                makespan_priority = start_time + processing_time #early completion
                balance_priority = machine_load[machine] #lower load better
                #adaptive weight based on progress
                progress_ratio = job_completion_time[job_id]/ sum([sum(times) for machines, times in jobs[job_id]]) if sum([sum(times) for machines, times in jobs[job_id]]) != 0 else 0
                alpha = 0.3 + progress_ratio * 0.4 # adjust weight: early stage favor balance, later stage favor makespan
                priority = alpha * makespan_priority + (1 - alpha) * balance_priority

                if priority < best_priority:
                    best_priority = priority
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        job_id, op_idx = best_operation
        machine, processing_time = best_machine

        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        machine_load[machine]+= processing_time #update machine load
        available_operations.remove((job_id, op_idx))

        # Add the next operation of the job if it exists
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    return schedule
