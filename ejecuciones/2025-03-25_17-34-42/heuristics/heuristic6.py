
def heuristic(input_data):
    """
    Schedules jobs using a shortest processing time first (SPTF) heuristic.
    Prioritizes operations with shorter processing times across all jobs.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}  # job finish time
    scheduled_operations = {} # Key is job, value is list of operations. Each operation is a dict with its attributes

    # Create a list of all operations with job and operation indices for sorting
    all_operations = []
    for job, operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on the minimum processing time available
    all_operations.sort(key=lambda op: min(op[3])) # Sort by shortest processing time

    for job, op_num, machines, times in all_operations:
        # Find the earliest possible start time for the operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the selected machine
        start_time = best_start_time
        end_time = start_time + best_processing_time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

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
