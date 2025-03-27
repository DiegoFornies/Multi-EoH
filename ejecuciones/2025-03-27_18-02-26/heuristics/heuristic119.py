
def heuristic(input_data):
    """Schedules operations based on earliest finish time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job_id in range(1, n_jobs + 1):
        eligible_operations.append((job_id, 0))

    scheduled_operations = set()

    while eligible_operations:
        best_op = None
        earliest_finish = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs[job_id][op_idx]

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                finish_time = start_time + processing_time

                if finish_time < earliest_finish:
                    earliest_finish = finish_time
                    best_op = (job_id, op_idx, machine, start_time, processing_time)

        job_id, op_idx, machine, start_time, processing_time = best_op
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
        job_completion_time[job_id] = end_time
        scheduled_operations.add((job_id, op_idx))

        eligible_operations = []
        for job_id in range(1, n_jobs + 1):
            next_op_idx = len(schedule.get(job_id, []))
            if next_op_idx < len(jobs[job_id]) and (job_id, next_op_idx) not in scheduled_operations:
                eligible_operations.append((job_id, next_op_idx))

    return schedule
