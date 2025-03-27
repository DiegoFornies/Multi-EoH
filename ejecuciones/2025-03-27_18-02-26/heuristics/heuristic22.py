
def heuristic(input_data):
    """
    A heuristic for FJSSP minimizing makespan and balancing machine load.
    Prioritizes operations with shorter processing times and less-loaded machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of operations and their corresponding job.
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })

    # Sort operations based on shortest processing time first
    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job = operation['job']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']
        op_num = op_idx + 1

        # Find the machine with the earliest available time among feasible machines.
        best_machine = None
        min_start_time = float('inf')
        processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = times[i]

        # Schedule the operation on the selected machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += processing_time
        job_completion_time[job] = end_time

    return schedule
