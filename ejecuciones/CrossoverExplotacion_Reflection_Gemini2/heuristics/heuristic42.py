
def heuristic(input_data):
    """Combines SPT and earliest available machine for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in jobs}

    for job_id in jobs:
        schedule[job_id] = []

    eligible_operations = []
    for job_id in jobs:
        eligible_operations.append((job_id, 0))

    while eligible_operations:
        best_op = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs[job_id][op_idx]

            for m_index, machine in enumerate(machines):
                processing_time = times[m_index]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_idx)
                    best_machine = (machine, processing_time)

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

            eligible_operations.remove(best_op)

            next_op_idx = op_idx + 1
            if next_op_idx < len(jobs[job_id]):
                eligible_operations.append((job_id, next_op_idx))
        else:
            break

    return schedule
