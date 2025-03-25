
def heuristic(input_data):
    """Combines earliest finish time and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    eligible_operations = []
    for job in range(1, n_jobs + 1):
        eligible_operations.append((job, 0)) # (job, operation_index)

    while eligible_operations:
        best_operation = None
        earliest_end_time = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]

            best_machine = -1
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                # Consider machine load
                weighted_end_time = end_time + machine_load[machine] * 0.1 

                if weighted_end_time < min_end_time:
                    min_end_time = weighted_end_time
                    best_machine = machine

            if min_end_time < earliest_end_time:
                earliest_end_time = min_end_time
                best_operation = (job, op_idx, best_machine, times[machines.index(best_machine)])

        job, op_idx, assigned_machine, processing_time = best_operation
        start_time = max(machine_available_time[assigned_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[assigned_machine] = end_time
        job_completion_time[job] = end_time
        machine_load[assigned_machine] += processing_time

        eligible_operations.remove((job, op_idx))

        if op_idx + 1 < len(jobs[job]):
            eligible_operations.append((job, op_idx + 1))
    return schedule
