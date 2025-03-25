
def heuristic(input_data):
    """Schedules jobs using SPT and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}
    scheduled_operations = set()

    eligible_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            eligible_operations.append((job_id, op_idx, machines, times))

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        best_operation = None
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for job_id, op_idx, machines, times in eligible_operations:
            if (job_id, op_idx) in scheduled_operations:
                continue

            preceding_operations_scheduled = True
            for prev_op_idx in range(op_idx):
                if (job_id, prev_op_idx) not in scheduled_operations:
                    preceding_operations_scheduled = False
                    break

            if not preceding_operations_scheduled:
                continue

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Primary: Minimize end time; Secondary: Balance machine load.
                if end_time < best_start_time + best_processing_time if best_operation else True:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_operation = (job_id, op_idx, machines, times)
                elif end_time == best_start_time + best_processing_time if best_operation else False:
                    if machine_load[machine] < machine_load[best_machine]:
                        best_start_time = start_time
                        best_machine = machine
                        best_processing_time = processing_time
                        best_operation = (job_id, op_idx, machines, times)
        if best_operation:
            job_id, op_idx, machines, times = best_operation
            operation_number = op_idx + 1
            end_time = best_start_time + best_processing_time
            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += best_processing_time
            scheduled_operations.add((job_id, op_idx))

    return schedule
