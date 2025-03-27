
def heuristic(input_data):
    """
    Schedules jobs by balancing machine load and minimizing job idle time,
    using a lookahead approach.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(n_jobs)}

    for job in range(n_jobs):
        schedule[job] = []

    # Iterate through all operations and select best machine
    operations = []
    for job_id, job_ops in jobs.items():
        for op_index, op_data in enumerate(job_ops):
            operations.append((job_id, op_index, op_data))

    # Sort operation according to shortest processing time from all possible
    operations.sort(key=lambda x: min(x[2][1]))

    for job_id, op_index, op_data in operations:
        machines, times = op_data
        op_num = op_index + 1

        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            # lookahead:  estimate the machine load after assigning operation and add
            # estimate to start time
            load_estimate = machine_load[machine] + processing_time
            start_time += load_estimate / 1000

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += best_processing_time
        job_completion_time[job_id] = end_time

    return schedule
