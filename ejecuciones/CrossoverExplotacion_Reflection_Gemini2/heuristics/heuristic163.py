
def heuristic(input_data):
    """Combines SPT, least loaded machine, and a delay factor for better FJSSP scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine, best_processing_time = None, float('inf')
        earliest_completion_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                completion_time = start_time + processing_time
                workload = machine_workload[machine_id]

                current_makespan = max(machine_available_times.values())
                delay_factor = (workload / (sum(machine_workload.values()) + 1e-6)) * (completion_time / (current_makespan + 1e-6)) * 5

                combined_metric = 0.6 * completion_time + 0.2 * (workload / (sum(machine_workload.values()) + 1e-6)) * 5 + 0.2 * delay_factor


                if combined_metric < earliest_completion_time:
                    earliest_completion_time = combined_metric
                    best_job, best_op_index = job_id, op_index
                    best_machine, best_processing_time = machine_id, processing_time

        job_id, op_index = best_job, best_op_index
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += best_processing_time

        ready_operations.remove((job_id, op_index))
        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
