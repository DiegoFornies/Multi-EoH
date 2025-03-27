
def heuristic(input_data):
    """
    A heuristic to schedule jobs on machines minimizing makespan.
    Uses a greedy approach with shortest processing time (SPT) rule.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}  # Store the scheduling result
    machine_available_time = {m: 0 for m in range(n_machines)} # Keep track of when each machine is available
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)} # Keep track of when each job is finished

    for job in jobs:
        schedule[job] = []

    # Iterate through all operations of all jobs and assign them to machine with shortest processing time
    operations = []
    for job in jobs:
        for op_idx, (machines, times) in enumerate(jobs[job]):
            operations.append((job, op_idx, machines, times))

    # Sort operations by the shortest processing time, consider a machine available and job finishing time
    operations.sort(key=lambda op: min(op[3]))  # Sort by minimum processing time

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the best machine for current operation
        best_machine = None
        min_end_time = float('inf')

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Update the schedule
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine available time and job finishing time
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time

    return schedule
