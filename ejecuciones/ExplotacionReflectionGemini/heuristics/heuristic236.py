
def heuristic(input_data):
    """Combines SPT and machine load balancing for FJSSP."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}

    eligible_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            eligible_operations.append((job_id, op_idx, machines, times))

    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        best_operation = None
        min_start_time = float('inf')

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

            best_machine = -1
            best_processing_time = float('inf')
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                elif start_time == min_start_time:
                    if machine_load[machine] < machine_load[best_machine] if best_machine != -1 else True:
                        best_machine = machine
                        best_processing_time = processing_time


            if best_machine != -1:
                best_operation = (job_id, op_idx, best_machine, min_start_time, best_processing_time)
                

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

    return schedule
