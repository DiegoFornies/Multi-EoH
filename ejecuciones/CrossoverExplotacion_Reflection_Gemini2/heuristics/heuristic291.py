
def heuristic(input_data):
    """Combines EFT, SPT, machine load balancing, and ready operation scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        min_combined_score = float('inf')

        for job_id, op_index in ready_operations:
            machines = jobs_data[job_id][op_index][0]
            processing_times = jobs_data[job_id][op_index][1]

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time

                weighted_finish = 0.6 * end_time + 0.4 * processing_time
                load_penalty = 0.01 * machine_workload[machine]
                combined_score = weighted_finish + load_penalty + machine * 0.0001

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_job = job_id
                    best_op_index = op_index
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time
                    best_end_time = end_time

        job_id = best_job
        op_index = best_op_index
        best_machine = best_machine
        best_processing_time = best_processing_time
        best_start_time = best_start_time
        best_end_time = best_end_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_end_time,
            'Processing Time': best_processing_time
        })

        machine_available[best_machine] = best_end_time
        job_completion[job_id] = best_end_time
        machine_workload[best_machine] += best_processing_time
        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
