
def heuristic(input_data):
    """Schedules jobs, balancing makespan & machine load (SPT + Workload)."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        min_combined_metric = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                completion_time = start_time + processing_time
                workload = machine_workload[machine_id]

                # Combine completion time and workload
                combined_metric = completion_time + (workload / (sum(machine_workload.values()) + 1e-6)) * 5 # Shortest Processing Time & workload consideration

                if combined_metric < min_combined_metric:
                    min_combined_metric = combined_metric
                    best_job, best_op_index = job_id, op_index
                    best_machine = machine_id
                    best_processing_time = processing_time
                    best_start_time = start_time
                    best_end_time = completion_time

        job_id, op_index = best_job, best_op_index
        start_time = best_start_time
        end_time = best_end_time
        machine_id = best_machine
        processing_time = best_processing_time

        machine_available_times[machine_id] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[machine_id] += processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': machine_id,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
