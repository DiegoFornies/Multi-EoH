
def heuristic(input_data):
    """Combines workload, earliest time, and SPT for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine, best_processing_time = None, float('inf')
        best_start_time = None
        min_weighted_finish = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for machine_id, processing_time in zip(machines, times):
                start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
                finish_time = start_time + processing_time

                weighted_finish = 0.5 * finish_time + 0.5 * machine_load[machine_id]
                
                if weighted_finish < min_weighted_finish:
                    min_weighted_finish = weighted_finish
                    best_job, best_op_index = job_id, op_index
                    best_machine, best_processing_time = machine_id, processing_time
                    best_start_time = start_time

        job_id, op_index = best_job, best_op_index

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time

        ready_operations.remove((job_id, op_index))
        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
