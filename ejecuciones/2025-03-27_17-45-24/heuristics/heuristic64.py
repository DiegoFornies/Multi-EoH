
def heuristic(input_data):
    """Schedules jobs by prioritizing operations with the least slack time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Calculate total processing time for each job
    job_total_processing_time = {}
    for job in range(1, n_jobs + 1):
        total_time = 0
        for machines, times in jobs_data[job]:
            total_time += min(times)  # optimistic estimate
        job_total_processing_time[job] = total_time

    # Create a list of operations and sort them by slack
    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs_data[job]):
            operations.append((job, op_idx))

    def calculate_slack(job, op_idx, machine):
        machines, times = jobs_data[job][op_idx]
        processing_time = times[machines.index(machine)]
        start_time = max(machine_available_time[machine], job_completion_time[job])

        remaining_time = job_total_processing_time[job]
        for i in range(op_idx + 1):
            remaining_time -= min(jobs_data[job][i][1]) if i != op_idx else processing_time  # Subtract previously scheduled + current
        # estimate of min process time of remaining operation.
        return start_time + processing_time + remaining_time # estimate makespan after scheduling current
    
    operations.sort(key=lambda item: min([calculate_slack(item[0], item[1], m) for m in jobs_data[item[0]][item[1]][0]]))

    # Schedule operations based on sorted order (least slack)
    for job, op_idx in operations:
        machines, times = jobs_data[job][op_idx]

        best_machine = None
        min_slack = float('inf')
        best_start_time = None
        best_processing_time = None

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            slack = calculate_slack(job, op_idx, machine)

            if slack < min_slack:
                min_slack = slack
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time
        job_total_processing_time[job] -= best_processing_time

    return schedule
