
def heuristic(input_data):
    """Combines SPT, machine load, and earliest start time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}
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
            preceding_operations_scheduled = all(
                (job_id, prev_op_idx) in scheduled_operations for prev_op_idx in range(op_idx)
            )
            if not preceding_operations_scheduled:
                continue
            eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        min_end_time = float('inf')  # Changed to end time
        min_start_time = float('inf') # Track the minimum start time

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                
                #Primary: Earliest End Time
                #Secondary: Least Loaded Machine
                if end_time < min_end_time:
                    min_end_time = end_time
                    min_start_time = start_time # Update minimum start time as well
                    best_machine = machine
                    best_operation = (job_id, op_idx, op_data, processing_time)
                elif end_time == min_end_time:
                    if machine_load[machine] < machine_load[best_machine]:
                        min_start_time = start_time
                        best_machine = machine
                        best_operation = (job_id, op_idx, op_data, processing_time)

        if best_operation:
            job_id, op_idx, op_data, processing_time = best_operation
            operation_number = op_idx + 1
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += processing_time
            scheduled_operations.add((job_id, op_idx))

    return schedule
