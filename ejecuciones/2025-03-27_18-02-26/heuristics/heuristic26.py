
def heuristic(input_data):
    """
    Heuristic for FJSSP minimizing makespan and balancing machine load.
    Schedules operations based on shortest processing time and earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_index, (machines, times) in enumerate(operations_list):
            operations.append((job_id, op_index + 1, machines, times))

    # Sort operations based on shortest processing time across possible machines.
    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_num, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')

        for machine_index, machine in enumerate(machines):
            processing_time = times[machine_index]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time
        
        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })

    return schedule
