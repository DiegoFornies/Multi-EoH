
def heuristic(input_data):
    """
    A heuristic to schedule jobs on machines, minimizing makespan.
    It assigns operations to machines based on earliest available time and shortest processing time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_assignments = {job: [] for job in range(1, n_jobs + 1)}

    schedule = {}
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    operations = {}
    for job_id, job_ops in jobs_data.items():
        operations[job_id] = []
        for i, op in enumerate(job_ops):
            operations[job_id].append((job_id, i + 1, op)) # job_id, op_num, (machines, times)

    available_operations = []
    for job_id in jobs_data.keys():
        available_operations.append(operations[job_id][0])

    scheduled_operations = set()

    while available_operations:
        # Find the operation that can start the earliest.
        best_operation = None
        earliest_start_time = float('inf')

        for op in available_operations:
            job_id, op_num, (machines, times) = op
            
            #Find the earliest start time on available machines
            min_start_time = float('inf')
            best_machine = None
            best_processing_time = None
            
            for machine_index, machine in enumerate(machines):
                available_time = max(machine_available_time[machine], job_completion_time[job_id])
                if available_time < min_start_time:
                    min_start_time = available_time
                    best_machine = machine
                    best_processing_time = times[machine_index]
            
            if min_start_time < earliest_start_time:
                earliest_start_time = min_start_time
                best_operation = op
                best_machine_choice = best_machine
                best_processing_time_choice = best_processing_time

        job_id, op_num, (machines, times) = best_operation

        start_time = max(machine_available_time[best_machine_choice], job_completion_time[job_id])
        processing_time = best_processing_time_choice
        end_time = start_time + processing_time

        machine_available_time[best_machine_choice] = end_time
        job_completion_time[job_id] = end_time

        machine_assignments[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine_choice,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
        })
        schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine_choice,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
        })
        scheduled_operations.add(best_operation)

        available_operations.remove(best_operation)

        # Add the next operation for the job to the available operations
        op_index = op_num
        if op_index < len(operations[job_id]):
            next_operation = operations[job_id][op_index]
            available_operations.append(next_operation)

    return schedule
