
def heuristic(input_data):
    """A heuristic for the FJSSP that aims to minimize makespan.

    It prioritizes operations with fewer machine choices and shorter processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations with their job and operation index.
    operations = []
    for job, ops in jobs_data.items():
        for i, op in enumerate(ops):
            operations.append((job, i))

    # Sort operations based on the number of available machines and processing time.
    operations.sort(key=lambda op: (len(jobs_data[op[0]][op[1]][0]),
                                      min(jobs_data[op[0]][op[1]][1])))

    for job, op_idx in operations:
        machines, times = jobs_data[job][op_idx]

        # Find the machine that allows the earliest completion time.
        best_machine = None
        earliest_start = float('inf')
        earliest_end = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + times[i]

            if end_time < earliest_end:
                earliest_end = end_time
                earliest_start = start_time
                best_machine = machine
                processing_time = times[i]

        # Schedule the operation on the best machine.
        if job not in schedule:
            schedule[job] = []

        op_num = op_idx + 1  # Corrected operation number calculation
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': earliest_start,
            'End Time': earliest_end,
            'Processing Time': processing_time
        })

        # Update machine and job completion times.
        machine_available_time[best_machine] = earliest_end
        job_completion_time[job] = earliest_end

    return schedule
