
def heuristic(input_data):
    """Heuristic for FJSSP: Combines EFT and load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []

    operation_queue = []
    for job, operations in jobs.items():
        operation_queue.append((job, 0))

    while operation_queue:
        job_id, op_index = operation_queue.pop(0)
        machines, times = jobs[job_id][op_index]

        best_machine = None
        min_end_time = float('inf')
        best_start_time = 0
        best_processing_time = 0

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], schedule[job_id][-1]['End Time'] if op_index > 0 else 0)
            end_time = start_time + processing_time

            # Load balancing factor
            load_factor = 1 + machine_load[machine] / (sum(machine_load.values()) + 1e-9)
            adjusted_end_time = end_time * load_factor

            if adjusted_end_time < min_end_time:
                min_end_time = adjusted_end_time
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

        if op_index + 1 < len(jobs[job_id]):
            operation_queue.append((job_id, op_index + 1))

    return schedule
