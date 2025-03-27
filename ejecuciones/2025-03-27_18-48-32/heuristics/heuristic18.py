
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine available times
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a list of operations to schedule, sorted by shortest processing time
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    operations.sort(key=lambda op: min(op[3])) # Sort by shortest processing time

    # Schedule each operation
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the machine that minimizes completion time of the operation
        best_machine, best_time = None, float('inf')
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + times[i]
            if end_time < best_time:
                best_time = end_time
                best_machine = machine
                processing_time = times[i]

        # Update the schedule
        if job not in schedule:
            schedule[job] = []

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time
        schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': processing_time})

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
