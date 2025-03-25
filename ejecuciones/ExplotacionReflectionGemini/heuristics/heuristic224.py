
def heuristic(input_data):
    """Schedules jobs considering machine load, job order, and idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    # Prioritize operations based on earliest start time on any machine.
    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))  # (job_id, operation_index)

    scheduled_operations = set()

    while available_operations:
        best_operation = None
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for job_id, op_idx in available_operations:
            machines, times = jobs_data[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + processing_time

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_operation = (job_id, op_idx)
                    best_machine = machine
                    best_processing_time = processing_time
                elif start_time == earliest_start_time:
                    if machine_load[machine] < machine_load[best_machine]:
                        best_operation = (job_id, op_idx)
                        best_machine = machine
                        best_processing_time = processing_time

        job_id, op_idx = best_operation
        machine = best_machine
        processing_time = best_processing_time

        start_time = max(machine_available_time[machine], job_last_end_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_last_end_time[job_id] = end_time
        machine_load[machine] += processing_time
        available_operations.remove((job_id, op_idx))

        # Add the next operation of the job if it exists
        if op_idx + 1 < len(jobs_data[job_id]):
            available_operations.append((job_id, op_idx + 1))

    return schedule
