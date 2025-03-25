
def heuristic(input_data):
    """Combines makespan minimization, balance improvement, and job sequencing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_operations = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()

    while any(remaining_operations[job] > 0 for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx in available_operations:
            if (job_id, op_idx) not in scheduled_operations:
                is_next_operation = True
                if op_idx > 0:
                    completed = False
                    for scheduled_op in schedule[job_id]:
                        if scheduled_op["Operation"] == op_idx:
                            completed = True
                            break
                    if not completed:
                        is_next_operation = False

                if is_next_operation:
                    eligible_operations.append((job_id, op_idx))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        min_score = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs[job_id][op_idx]
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                #Heuristic score. Machine load is important for balance.
                score = start_time + processing_time # minimize start and processing time, and balance the load
                if score < min_score:
                    min_score = score
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        if best_operation:
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
            scheduled_operations.add((job_id, op_idx))
            remaining_operations[job_id] -= 1

            if op_idx + 1 < len(jobs[job_id]):
                available_operations[job_id-1] = (job_id, op_idx + 1)

    return schedule
