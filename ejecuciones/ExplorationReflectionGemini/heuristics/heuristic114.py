
def heuristic(input_data):
    """Schedules jobs by iteratively assigning operations to minimize makespan and balance machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    remaining_operations = {job_id: 0 for job_id in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        remaining_operations[job_id] = len(jobs[job_id])

    unassigned_operations = []
    for job_id in range(1, n_jobs + 1):
        for operation_index in range(len(jobs[job_id])):
            unassigned_operations.append((job_id, operation_index))

    while unassigned_operations:
        best_operation = None
        best_machine = None
        min_makespan_increase = float('inf')
        
        for job_id, operation_index in unassigned_operations:
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]
            
            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                available_time = machine_available_times[machine]
                previous_completion_time = job_completion_times[job_id]
                start_time = max(available_time, previous_completion_time)
                end_time = start_time + processing_time
                
                makespan_increase = max(0, end_time - max(machine_available_times[machine], max(job_completion_times.values())))
                
                if makespan_increase < min_makespan_increase:
                    min_makespan_increase = makespan_increase
                    best_operation = (job_id, operation_index)
                    best_machine = machine
                    best_start_time = start_time
                    best_end_time = end_time
                    best_processing_time = processing_time
        
        job_id, operation_index = best_operation
        machine = best_machine

        machine_available_times[machine] = best_end_time
        job_completion_times[job_id] = best_end_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': machine,
            'Start Time': best_start_time,
            'End Time': best_end_time,
            'Processing Time': best_processing_time
        })

        unassigned_operations.remove(best_operation)
    return schedule
