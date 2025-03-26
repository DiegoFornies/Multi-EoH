
def heuristic(input_data):
    """Schedule using dynamic job priority and SPT."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    job_priority = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job priorities

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    remaining_operations = sum(len(job_ops) for job_ops in jobs.values())
    
    while remaining_operations > 0:
        eligible_operations = []
        for job_id in range(1, n_jobs + 1):
            if len(schedule[job_id]) < len(jobs[job_id]):
                operation_index = len(schedule[job_id])
                operation_data = jobs[job_id][operation_index]
                eligible_operations.append((job_id, operation_index, operation_data))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, operation_index, operation_data in eligible_operations:
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Dynamic job priority: increase priority if waiting for too long
            job_priority[job_id] += 0.01 # small increment.

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time

                # Heuristic: SPT + Job Priority. Lower end_time and higher job priority win
                priority_score = end_time - job_priority[job_id] 
                
                if priority_score < min_end_time:
                    min_end_time = priority_score
                    best_operation = (job_id, operation_index, operation_data)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        if best_operation:
            job_id, operation_index, operation_data = best_operation

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available[best_machine] = best_start_time + best_processing_time
            job_completion[job_id] = best_start_time + best_processing_time
            remaining_operations -= 1
        else:
            break # Prevent infinite loop if no operation can be scheduled

    return schedule
