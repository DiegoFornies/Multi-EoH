
def heuristic(input_data):
    """Combines SPT, min workload, and earliest available time for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    while operations:
        # Prioritize operations based on earliest start time on least loaded machine
        best_operation = None
        best_machine = None
        min_combined_score = float('inf')

        for operation in operations:
            job_id = operation['job']
            op_num = operation['operation']
            machines = operation['machines']
            times = operation['times']

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + processing_time

                # Combine workload and earliest availabiliy
                combined_score = machine_load[machine] + end_time
                
                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_operation = operation
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

        if best_operation is None:
            break
        
        job_id = best_operation['job']
        op_num = best_operation['operation']

        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time
        job_last_end_time[job_id] = best_start_time + best_processing_time
        operations.remove(best_operation)

    return schedule
