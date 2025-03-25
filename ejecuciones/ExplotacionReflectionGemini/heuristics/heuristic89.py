
def heuristic(input_data):
    """Combines earliest availability & job priority for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {machine: 0 for machine in range(n_machines)}

    job_priority = {job_id: len(jobs[job_id]) for job_id in range(1, n_jobs + 1)}
    eligible_operations = []
    for job, operations in jobs.items():
        eligible_operations.append((job, 0))

    while eligible_operations:
        best_operation = None
        earliest_end_time = float('inf')
        
        # Prioritize jobs with smaller number of operations
        sorted_eligible_operations = sorted(eligible_operations, key=lambda x: job_priority[x[0]])

        for job, op_idx in sorted_eligible_operations:
            machines, times = jobs[job][op_idx]
            
            best_machine, min_end_time = -1, float('inf')
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = time

                elif end_time == min_end_time and machine_load[machine] < machine_load[best_machine]:
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = time

            if min_end_time < earliest_end_time:
                earliest_end_time = min_end_time
                best_operation = (job, op_idx, best_machine, best_start_time, best_processing_time)

        job, op_idx, assigned_machine, start_time, processing_time = best_operation
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
