
def heuristic(input_data):
    """FJSSP heuristic: Combines earliest finish time with machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    eligible_operations = []
    for job in jobs:
        eligible_operations.append((job, 0))

    while eligible_operations:
        best_operation = None
        earliest_end_time = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                # Combine earliest end time with machine load
                score = end_time + machine_load[machine] * 0.1 

                if score < earliest_end_time:
                    earliest_end_time = score
                    best_operation = (job, op_idx, machine, start_time, processing_time)

        if best_operation:
            job, op_idx, machine, start_time, processing_time = best_operation
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job] = end_time
            machine_load[machine] += processing_time

            eligible_operations.remove((job, op_idx))

            if op_idx + 1 < len(jobs[job]):
                eligible_operations.append((job, op_idx + 1))

    return schedule
