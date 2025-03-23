
def heuristic(input_data):
    """Schedules jobs balancing makespan, separation, workload using combined scores."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}
    job_start_times = {j: [] for j in range(1, n_jobs + 1)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        min_combined_score = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine_id in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time

                # Separation Incentive
                separation_incentive = 0
                if job_start_times[job_id]:
                    last_start_time = job_start_times[job_id][-1]
                    separation_incentive = max(0, (start_time - last_start_time)) * 0.05

                # Workload balancing
                workload_factor = machine_workload[machine_id] * 0.01

                # Makespan impact
                makespan_factor = end_time / (max(machine_available_times.values()) + 1e-6) * 0.1 if machine_available_times else 0

                combined_score = 0.4 * end_time + 0.3 * workload_factor + 0.2 * makespan_factor - 0.1 * separation_incentive

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_job = job_id
                    best_op_index = op_index
                    best_machine = machine_id
                    best_processing_time = processing_time
                    best_start_time = start_time

        job_id, op_index = best_job, best_op_index
        best_machine, best_processing_time, best_start_time = best_machine, best_processing_time, best_start_time

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += best_processing_time
        job_start_times[job_id].append(start_time)

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
