
def heuristic(input_data):
    """Combines EFT with dynamic priority adjustments for balanced FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    operation_queue = []
    for job, operations in jobs.items():
        operation_queue.append((job, 0))

    while operation_queue:
        job_id, op_index = operation_queue.pop(0)
        machines_available, times_available = jobs[job_id][op_index]

        best_machine, best_start_time, best_processing_time, best_priority = None, float('inf'), None, float('inf')

        for m_index, machine in enumerate(machines_available):
            processing_time = times_available[m_index]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            finish_time = start_time + processing_time

            # Dynamic Priority: Combines Makespan and Load Balancing
            makespan_impact = finish_time
            load_imbalance = abs(machine_load[machine] - (sum(machine_load.values()) / n_machines if sum(machine_load.values()) else 0))
            priority = makespan_impact + 0.5 * load_imbalance

            if priority < best_priority:
                best_priority = priority
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        operation = {
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        }
        schedule[job_id].append(operation)

        machine_available_time[best_machine] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

        if op_index + 1 < len(jobs[job_id]):
            operation_queue.append((job_id, op_index + 1))

    return schedule
