
def heuristic(input_data):
    """FJSSP heuristic: Combines shortest processing time & machine load balancing."""
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

    while any(len(schedule[job]) < len(jobs[job]) for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if (job_id in schedule) and (len(schedule[job_id]) > op_idx): # operation already scheduled, skip
                continue

            if (job_id not in schedule) or (len(schedule[job_id]) < op_idx):  # previous operation is not scheduled.
                if op_idx > 0: # operation depends on the previous
                    scheduled_count = 0
                    for scheduled_op in schedule[job_id]:
                      if scheduled_op['Operation'] == op_idx: # previous op has been scheduled
                        scheduled_count = 1

                    if (scheduled_count < 1) and (op_idx > 0): # if previous has not been scheduled
                        continue

            if job_id not in schedule:
              schedule[job_id] = []

            if len(schedule[job_id]) == op_idx:  # check if it is the next
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

                # Score considers idle time and machine load. Prioritize lower loaded machines
                score = start_time + machine_load[machine] * 0.1 + processing_time

                if score < min_score:
                    min_score = score
                    best_operation = (job_id, op_idx, machine, start_time, processing_time)

        if best_operation:
            job_id, op_idx, machine, start_time, processing_time = best_operation
            end_time = start_time + processing_time
            operation_number = op_idx + 1
            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[machine] += processing_time
            scheduled_operations.add((job_id, op_idx))

        else:
            break

    return schedule
