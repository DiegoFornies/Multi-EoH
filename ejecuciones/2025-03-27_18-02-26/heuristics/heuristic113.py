
def heuristic(input_data):
    """Combines SPT, least loaded machine, and job prioritization."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_index, operation in enumerate(operations):
            eligible_machines = operation[0]
            processing_times = operation[1]

            # Choose machine based on SPT and least loaded
            best_machine = None
            min_combined_metric = float('inf')

            for machine_index, machine_id in enumerate(eligible_machines):
                time = processing_times[machine_index]
                machine_load = machine_time[machine_id]  # Use machine_time

                # Combine SPT and machine load (weighted)
                combined_metric = time + 0.1 * machine_load  # Adjust weight
                
                if combined_metric < min_combined_metric:
                    min_combined_metric = combined_metric
                    best_machine = machine_id
                    best_processing_time = time

            start_time = max(machine_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_time[best_machine] = end_time  # Update machine_time
            job_completion_time[job_id] = end_time

    return schedule
