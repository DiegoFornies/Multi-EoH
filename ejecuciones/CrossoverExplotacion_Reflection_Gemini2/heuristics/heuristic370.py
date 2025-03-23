
def heuristic(input_data):
    """Combines earliest finish time, SPT, and load balancing."""
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
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine_id in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available[machine_id]
                start_time = max(available_time, job_completion[job_id])
                end_time = start_time + processing_time

                # SPT and Earliest Finish Time
                weighted_finish = 0.6 * end_time + 0.4 * processing_time

                # Load balancing component with relative workload
                total_workload = sum(machine_workload.values())
                if total_workload > 0:
                    relative_workload = machine_workload[machine_id] / total_workload
                else:
                    relative_workload = 0  # Avoid division by zero

                load_penalty = relative_workload * 10  # Adjust penalty weight as needed
                combined_score = weighted_finish + load_penalty + machine_id * 0.0001

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_job, best_op_index = job_id, op_index
                    best_machine = machine_id
                    best_processing_time = processing_time
                    best_start_time = start_time

        job_id, op_index = best_job, best_op_index

        start_time = max(machine_available[best_machine], job_completion[job_id])
        end_time = start_time + best_processing_time

        machine_available[best_machine] = end_time
        job_completion[job_id] = end_time
        machine_workload[best_machine] += best_processing_time

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
