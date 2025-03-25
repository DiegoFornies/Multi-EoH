
def heuristic(input_data):
    """
    Aims to minimize makespan by prioritizing operations with shorter processing times
    and selecting machines with earlier available times.
    """
    schedule = {}
    machine_available_time = {m: 0 for m in range(input_data['n_machines'])}
    job_completion_time = {j: 0 for j in input_data['jobs']}

    # Create a list of operations with their possible machines and times
    operations = []
    for job, ops in input_data['jobs'].items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append({
                'job': job,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    # Sort operations by shortest processing time first
    operations.sort(key=lambda op: min(op['times']))

    # Assign operations to machines
    for operation in operations:
        job = operation['job']
        op_num = operation['operation']
        machines = operation['machines']
        times = operation['times']

        # Find the machine with the earliest available time for this operation
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_time = processing_time

        # Assign the operation to the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
