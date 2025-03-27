
def heuristic(input_data):
    """Schedules jobs by Earliest Due Date and least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    job_deadlines = {}
    for job in range(1, n_jobs + 1):
      total_time = 0
      for op in jobs[job]:
        total_time+= min(op[1])
      job_deadlines[job] = total_time * 2 # arbitrary deadline

    scheduled_count = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_count < total_operations:
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if len(schedule[job]) < len(jobs[job]):
                eligible_operations.append(job)

        if not eligible_operations:
            break

        # Prioritize jobs with earlier due dates
        urgent_job = min(eligible_operations, key=lambda job: job_deadlines[job] - job_completion_time[job])

        op_index = len(schedule[urgent_job])
        machines, times = jobs[urgent_job][op_index]

        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        # Select least loaded machine
        machine_load = {m: machine_available_time[m] for m in range(n_machines)}
        available_machines = [(m, times[machines.index(m)]) for m in machines]
        if not available_machines:
            break
        least_loaded_machine = min(available_machines, key=lambda x: machine_load[x[0]])[0]
        best_processing_time = times[machines.index(least_loaded_machine)]
        best_start_time = max(machine_available_time[least_loaded_machine], job_completion_time[urgent_job])
        best_machine = least_loaded_machine
        # Perform assignment
        operation = {
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        }
        schedule[urgent_job].append(operation)

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[urgent_job] = best_start_time + best_processing_time
        scheduled_count += 1

    return schedule
