
def heuristic(input_data):
    """Dynamic priority dispatching with lookahead."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    remaining_job_operations = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    completed_jobs = set()
    runnable_operations = []
    for job_id in range(1, n_jobs + 1):
        if job_id not in completed_jobs:
            runnable_operations.append((job_id, 0)) # (job_id, operation_index)

    while runnable_operations:
        best_op = None
        best_machine = None
        best_start_time = None
        best_processing_time = None
        min_priority = float('inf')

        for job_id, operation_index in runnable_operations:
            possible_machines = jobs[job_id][operation_index][0]
            possible_times = jobs[job_id][operation_index][1]

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])

                # Priority: (Makespan + Machine Load) / Remaining Operations
                priority = (start_time + processing_time + 0.1 * machine_available_times[machine]) / remaining_job_operations[job_id]
                
                if priority < min_priority:
                    min_priority = priority
                    best_op = (job_id, operation_index)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        job_id, operation_index = best_op
        
        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time
        remaining_job_operations[job_id] -= 1

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        runnable_operations.remove((job_id, operation_index))

        # Add the next operation of the scheduled job
        next_op_index = operation_index + 1
        if next_op_index < len(jobs[job_id]):
            runnable_operations.append((job_id, next_op_index))

        #Remove completed jobs:
        for job_id in range(1,n_jobs +1):
            if remaining_job_operations[job_id] == 0:
                completed_jobs.add(job_id)
    return schedule
