
def heuristic(input_data):
    """
    Heuristic for FJSSP scheduling. Prioritizes operations with fewer machine options and shorter processing times
    to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {}

    # Create a list of operations with job and operation index for sorting
    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_index, op_data in enumerate(operations_list):
            operations.append((job_id, op_index, op_data))

    # Sort operations based on number of available machines and processing time
    operations.sort(key=lambda x: (len(x[2][0]), min(x[2][1])))

    for job_id, op_index, op_data in operations:
        machines, times = op_data

        # Find the earliest available machine and its corresponding start time
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the selected machine
        start_time = min_start_time
        end_time = start_time + best_processing_time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        # Update the schedule
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

    return schedule
