
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules operations based on shortest processing time and earliest available machine.
    Prioritizes minimizing makespan by considering both machine and job idle times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}

    # Keep track of unscheduled operations for each job
    unscheduled_operations = {j: 0 for j in jobs_data}
    for job_id in jobs_data:
        unscheduled_operations[job_id] = 0

    # total number of operations
    total_ops = 0
    for job_id in jobs_data:
        total_ops += len(jobs_data[job_id])

    scheduled_ops = 0
    while scheduled_ops < total_ops:
        best_job, best_op, best_machine, best_start_time, best_processing_time = None, None, None, float('inf'), None

        for job_id, operations in jobs_data.items():
            if unscheduled_operations[job_id] >= len(operations):
                continue

            op_idx = unscheduled_operations[job_id]
            machines, times = operations[op_idx]
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_job = job_id
                    best_op = op_idx
                    best_machine = machine
                    best_processing_time = processing_time

        # Schedule the best operation
        if best_job is not None:
            job_id = best_job
            op_idx = best_op
            machine = best_machine
            start_time = best_start_time
            processing_time = best_processing_time
            
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
            unscheduled_operations[job_id] += 1
            scheduled_ops += 1

    return schedule
