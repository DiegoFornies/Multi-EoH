
def heuristic(input_data):
    """
    Heuristic scheduler for FJSSP. Prioritizes operations with shortest processing time and earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    eligible_operations = []
    for job_id in jobs_data:
        eligible_operations.append((job_id, 0))  # (job_id, operation_index)

    scheduled_operations = set()

    while eligible_operations:
        best_op = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs_data[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + times[machine_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_idx)
                    best_machine = (machine, times[machine_idx])

        if best_op is not None:
            job_id, op_idx = best_op
            machine, processing_time = best_machine

            start_time = max(machine_available_time[machine], job_last_end_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_last_end_time[job_id] = end_time
            scheduled_operations.add(best_op)
        
            eligible_operations.remove(best_op)

            next_op_idx = op_idx + 1
            if next_op_idx < len(jobs_data[job_id]):
                eligible_operations.append((job_id, next_op_idx))
        else:
            break # Should not happen, but for safety.
            
    return schedule
