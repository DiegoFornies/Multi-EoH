
def heuristic(input_data):
    """Schedules jobs considering machine availability and job completion."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    while available_operations:
        best_op = None
        min_score = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]
            remaining = len(jobs[job_id]) - op_idx

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                score = remaining + start_time #Prioritize jobs with fewer remaining and minimal idle time

                if score < min_score:
                    min_score = score
                    best_op = (job_id, op_idx, machine, start_time, processing_time)

        if best_op:
            job_id, op_idx, machine, start_time, processing_time = best_op
            end_time = start_time + processing_time

            if job_id not in schedule:
                schedule[job_id] = []
            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time

            available_operations.remove((job_id, op_idx))
            if op_idx + 1 < len(jobs[job_id]):
                available_operations.append((job_id, op_idx + 1))
        else:
            break

    return schedule
