
def heuristic(input_data):
    """Combines EFT and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    operation_queue = []
    for job in jobs:
        schedule[job] = []
        operation_queue.append((job, 0))

    while operation_queue:
        job_id, op_index = operation_queue.pop(0)
        machines, times = jobs[job_id][op_index]

        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            finish_time = start_time + processing_time
            load_factor = machine_load[machine]

            if finish_time + 0.1*load_factor < best_start_time:
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time
                best_finish_time = finish_time

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
