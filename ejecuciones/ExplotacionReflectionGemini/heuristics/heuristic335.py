
def heuristic(input_data):
    """Combines SPT and machine load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    eligible_operations = []
    for job, operations in jobs.items():
        eligible_operations.append((job, 0))

    while eligible_operations:
        best_operation = None
        min_combined_score = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]
            
            best_machine = -1
            best_start_time = float('inf')
            best_processing_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                
                # Primary: SPT, Secondary: load balancing.
                combined_score = start_time + machine_load[machine]

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_operation = (job, op_idx, machine, time, start_time)
        
        job, op_idx, assigned_machine, processing_time, start_time = best_operation
        end_time = start_time + processing_time
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[assigned_machine] = end_time
        job_completion_time[job] = end_time
        machine_load[assigned_machine] += processing_time

        eligible_operations.remove((job, op_idx))

        if op_idx + 1 < len(jobs[job]):
            eligible_operations.append((job, op_idx + 1))

    return schedule
