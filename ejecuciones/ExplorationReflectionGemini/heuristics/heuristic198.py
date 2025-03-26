
def heuristic(input_data):
    """Schedules jobs using a dynamic priority rule adapting to machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}

    runnable_operations = []
    for job_id in range(1, n_jobs + 1):
        runnable_operations.append({'job': job_id, 'op_idx': 0})

    while runnable_operations:
        best_op = None
        best_machine = None
        min_combined_score = float('inf')

        for op_data in runnable_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                completion_time = start_time + processing_time
                load_factor = machine_load[machine]

                # Dynamic priority: Weighs completion time and load based on overall load
                total_load = sum(machine_load.values())
                if total_load == 0:
                    load_weight = 0.1  # Initial bias towards load balancing
                else:
                    load_weight = total_load / (sum(times)/len(times)) if (sum(times)/len(times))!=0 else 0.1 # Adjust weighting based on total load and average duration

                combined_score = completion_time + load_weight * load_factor

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_op = op_data
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        # Schedule the chosen operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine load, availability, and job completion
        machine_load[best_machine] += best_processing_time
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

        # Update runnable operations
        runnable_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            runnable_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
