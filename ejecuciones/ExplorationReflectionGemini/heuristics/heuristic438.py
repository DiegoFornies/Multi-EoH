
def heuristic(input_data):
    """Schedules jobs minimizing makespan via earliest start time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    unassigned_operations = []
    for job_id in range(1, n_jobs + 1):
        for operation_index, operation_data in enumerate(jobs[job_id]):
            unassigned_operations.append((job_id, operation_index + 1))

    while unassigned_operations:
        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_processing_time = None
        
        for job_id, op_num in unassigned_operations:
            operation_index = op_num - 1
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = (job_id, op_num)
                    best_machine = machine
                    best_processing_time = processing_time

        job_id, op_num = best_op
        operation_index = op_num - 1
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time
        
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        unassigned_operations.remove((job_id, op_num))

    return schedule
