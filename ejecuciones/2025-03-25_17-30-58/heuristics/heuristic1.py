
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations based on shortest processing time (SPT)
    among available machines and schedules them on the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    
    eligible_operations = []
    for job_id in range(1, n_jobs + 1):
        eligible_operations.append((job_id, 0)) # (job_id, op_index)
        schedule[job_id] = []

    scheduled_operations = set()

    while eligible_operations:
        # Find the eligible operation with the shortest possible processing time
        best_op = None
        min_processing_time = float('inf')

        for job_id, op_index in eligible_operations:
            machines, times = jobs_data[job_id][op_index]
            current_min_time = min(times)
            if current_min_time < min_processing_time:
                min_processing_time = current_min_time
                best_op = (job_id, op_index)

        if not best_op:
            break
        
        job_id, op_index = best_op
        machines, times = jobs_data[job_id][op_index]

        # Find the machine that allows the earliest start time for the operation
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = times[i]
        
        # Schedule the operation on the selected machine
        start_time = earliest_start_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        eligible_operations.remove((job_id, op_index))

        # Add the next operation of the job to the eligible operations
        if op_index + 1 < len(jobs_data[job_id]):
            eligible_operations.append((job_id, op_index + 1))
            
    return schedule
