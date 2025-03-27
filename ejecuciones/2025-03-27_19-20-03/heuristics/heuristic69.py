
def heuristic(input_data):
    """Prioritizes shortest operations on least loaded machines."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_schedules = {m: [] for m in range(n_machines)}

    operation_queue = []
    for job in range(1, n_jobs + 1):
        operation_queue.append((job, 0))  # (job_id, op_index)

    while operation_queue:
        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_index in operation_queue:
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_load[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

        job_id, op_index = best_operation

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_schedules[best_machine].append({
            'Job': job_id,
            'Operation': op_index + 1,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_load[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

        operation_queue.remove(best_operation)

        if op_index + 1 < len(jobs_data[job_id]):
            operation_queue.append((job_id, op_index + 1))

    return schedule
