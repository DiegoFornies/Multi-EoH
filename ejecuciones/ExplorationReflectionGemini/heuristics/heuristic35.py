
def heuristic(input_data):
    """Schedules jobs greedily based on shortest processing time first."""
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}
    schedule = {}

    # Sort operations by shortest processing time
    operations = []
    for job, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job, op_idx + 1, machines, times))

    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        best_machine, best_time = None, float('inf')
        current_job_ops = jobs_data[job]
        op_idx = op_num -1

        # Find machine and time combination that results in earliest end time
        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job])
            end_time = start_time + processing_time
            if end_time < best_time:
                best_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        #Update Schedule
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_time,
            'Processing Time': best_processing_time
        })

        #Update Machine Available Time and Job Completion Time
        machine_available_times[best_machine] = best_time
        job_completion_times[job] = best_time

    return schedule
