
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with fewer machine choices
    and assigns them to the machine with the earliest available time.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}
    schedule = {}
    
    # Create a list of operations with job and operation index
    operations = []
    for job, ops in jobs_data.items():
        for i, op in enumerate(ops):
            operations.append((job, i, op))

    # Sort operations by the number of possible machines (ascending)
    operations.sort(key=lambda x: len(x[2][0]))

    for job, op_idx, operation_data in operations:
        machines, times = operation_data
        op_num = op_idx + 1

        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        earliest_start = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_time[machine], job_completion_times[job])
            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_processing_time = times[i]

        # If no feasible machine is found (should not happen), skip the operation
        if best_machine is None:
            continue

        start_time = earliest_start
        end_time = start_time + best_processing_time

        # Update machine and job completion times
        machine_time[best_machine] = end_time
        job_completion_times[job] = end_time

        # Add operation to the schedule
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

    return schedule
