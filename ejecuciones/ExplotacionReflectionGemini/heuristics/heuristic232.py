
def heuristic(input_data):
    """A heuristic for FJSSP combining shortest processing time and machine load balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set()

    while True:
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if (job_id, op_idx) not in scheduled_operations:
                is_next_operation = True
                if op_idx > 0:
                    scheduled = False
                    for sch_op in schedule[job_id]:
                        if sch_op['Operation'] == op_idx:
                            scheduled = True
                            break

                    if not scheduled:
                         is_next_operation = False
                if is_next_operation:
                    eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        min_score = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Score: prioritize shorter processing times and lower machine load.
                score = processing_time + 0.1 * machine_load[machine] + start_time *0.05 #added starttime

                if score < min_score:
                    min_score = score
                    best_operation = (job_id, op_idx, machine, start_time, processing_time)

        if best_operation:
            job_id, op_idx, machine, start_time, processing_time = best_operation
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
            scheduled_operations.add((job_id, op_idx))
            machine_load[machine] += processing_time
        else:
            break

    return schedule
