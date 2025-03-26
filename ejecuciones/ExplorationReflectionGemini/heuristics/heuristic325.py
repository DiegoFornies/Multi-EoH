
def heuristic(input_data):
    """FJSSP heuristic: Combines SPT, load balancing, and lookahead."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_remaining_work = {}

    for job, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)
        job_remaining_work[job] = total_time

    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        eligible_operations = []
        for job in jobs:
            op_index = job_operations_scheduled[job]
            if op_index < len(jobs[job]):
                eligible_operations.append((job, op_index))

        # Sort eligible operations by SPT and earliest availability
        eligible_operations.sort(key=lambda x: (job_remaining_work[x[0]], job_completion_times[x[0]]))

        for job, op_index in eligible_operations:
            machines, times = jobs[job][op_index]
            op_num = op_index + 1

            best_machine = None
            min_completion_time = float('inf')
            processing_time = None

            for i, m in enumerate(machines):
                available_time = machine_load[m]
                start_time = max(job_completion_times[job], available_time)
                end_time = start_time + times[i]

                # Lookahead: factor in future machine load
                estimated_future_load = machine_load[m]  # Simple version: current load
                completion_time = end_time + 0.01*estimated_future_load  # Adding weight for load balancing

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = m
                    processing_time = times[i]

            if best_machine is not None:
                start_time = max(job_completion_times[job], machine_load[best_machine])
                end_time = start_time + processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_times[job] = end_time
                job_remaining_work[job] -= processing_time  # Update remaining work
                job_operations_scheduled[job] += 1

    return schedule
