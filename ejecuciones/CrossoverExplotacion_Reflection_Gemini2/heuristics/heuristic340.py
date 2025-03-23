
def heuristic(input_data):
    """Schedules jobs minimizing makespan, separation, and workload balance. Prioritizes operations with fewer machine choices and dynamically adjusts weights."""
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
        best_machine = None
        min_combined_score = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            # Prioritize operations with fewer machine choices
            machine_choice_priority = 1 / len(machines) if len(machines) > 0 else 0

            for m_idx, machine_id in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time

                # Calculate workload imbalance penalty
                workload_penalty = machine_workload[machine_id] / (sum(machine_workload.values()) + 1e-6) if sum(machine_workload.values()) > 0 else 0
                
                # Calculate separation incentive: encourage jobs to spread across machines
                separation_incentive = 0
                if job_completion_times[job_id] > 0:
                    for prev_op in schedule[job_id]:
                        if prev_op['Assigned Machine'] == machine_id:
                            separation_incentive = 10  # Penalty if same machine used consecutively

                # Dynamically adjust weights based on problem characteristics
                makespan_weight = 1.0
                workload_weight = 0.5
                separation_weight = 0.2
                choice_weight = 0.1 #Weight to machine choice priority

                combined_score = (
                    makespan_weight * end_time
                    + workload_weight * workload_penalty
                    - separation_weight * separation_incentive
                    - choice_weight * machine_choice_priority #Incorporate machine choice
                )

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_job = job_id
                    best_op_index = op_index
                    best_machine = machine_id
                    best_start_time = start_time
                    best_end_time = end_time
                    best_processing_time = processing_time

        # Schedule the best operation on the best machine
        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[best_job] = end_time
        machine_workload[best_machine] += best_processing_time

        schedule[best_job].append({
            'Operation': best_op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        ready_operations.remove((best_job, best_op_index))

        if best_op_index + 1 < len(jobs_data[best_job]):
            ready_operations.append((best_job, best_op_index + 1))

    return schedule
