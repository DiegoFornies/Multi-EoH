
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes shorter processing times and available machines
    to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Stores operations with assigned job number to schedule based on priority
    operations_to_schedule = []
    for job_id, operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations):
            operations_to_schedule.append({
                'job': job_id,
                'operation_index': op_idx,
                'machines': machines,
                'times': times
            })

    # Sort operations by shortest processing time
    operations_to_schedule.sort(key=lambda x: min(x['times']))

    for operation in operations_to_schedule:
        job_id = operation['job']
        op_idx = operation['operation_index']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        # Find the best machine to process the operation
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[m_idx]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[m_idx]

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,  # Operation number
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
