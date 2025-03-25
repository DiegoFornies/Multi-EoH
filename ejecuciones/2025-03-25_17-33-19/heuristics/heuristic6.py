
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes jobs with fewer remaining operations
    and assigns operations to machines based on earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data.keys()}
    remaining_operations = {j: len(ops) for j, ops in jobs_data.items()}

    unscheduled_operations = []
    for job, operations in jobs_data.items():
        for i, operation in enumerate(operations):
            unscheduled_operations.append((job, i + 1, operation))

    # Sort operations based on job's remaining operations (fewer first)
    unscheduled_operations.sort(key=lambda x: remaining_operations[x[0]])

    while unscheduled_operations:
        best_op = None
        best_machine = None
        earliest_start = float('inf')

        # Find the best operation and machine to schedule it on
        for job, op_num, operation in unscheduled_operations:
            machines, times = operation
            for m, t in zip(machines, times):
                start_time = max(machine_available_time[m], job_completion_time[job])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = (job, op_num, operation)
                    best_machine = m
                    best_time = t

        # Schedule the best operation
        job, op_num, operation = best_op
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
        remaining_operations[job] -= 1

        # Remove the scheduled operation from unscheduled list
        unscheduled_operations.remove(best_op)
        unscheduled_operations.sort(key=lambda x: remaining_operations[x[0]])
    return schedule
