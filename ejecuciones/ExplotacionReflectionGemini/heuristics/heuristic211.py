
def heuristic(input_data):
    """
    Combines shortest processing time and earliest machine availability,
    prioritizing operations with shorter times on less loaded machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    scheduled_operations = set()

    operations = []
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if (job_id, op_idx) in scheduled_operations:
                continue

            preceding_operations_scheduled = True
            for prev_op_idx in range(op_idx):
                if (job_id, prev_op_idx) not in scheduled_operations:
                    preceding_operations_scheduled = False
                    break

            if not preceding_operations_scheduled:
                continue

            eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        best_start_time = float('inf')
        best_machine = None
        best_processing_time = None

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                # Prioritize machines with earlier availability
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = time
                    best_operation = (job_id, op_idx, op_data)

        if best_operation:
            job_id, op_idx, op_data = best_operation
            op_num = op_idx + 1
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            scheduled_operations.add((job_id, op_idx))

    return schedule
