
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    eligible_operations = {}
    for job in range(1, n_jobs + 1):
        eligible_operations[job] = 1

    scheduled_operations = 0
    while scheduled_operations < sum(len(ops) for ops in jobs.values()):
        # Find the next operation to schedule
        candidates = []
        for job in range(1, n_jobs + 1):
            if job in eligible_operations and eligible_operations[job] <= len(jobs[job]):
                candidates.append(job)

        if not candidates:
            break

        best_job = None
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for job in candidates:
            operation_index = eligible_operations[job] - 1
            machines, times = jobs[job][operation_index]

            # Find the best machine to schedule the operation on
            for m_index, machine in enumerate(machines):
                processing_time = times[m_index]
                start_time = max(machine_load[machine], job_completion_times[job])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_job = job
                    best_machine = machine
                    best_processing_time = processing_time

        # Schedule the operation
        if best_job is not None:
            job = best_job
            machine = best_machine
            processing_time = best_processing_time
            start_time = best_start_time

            operation_index = eligible_operations[job] - 1
            operation_number = operation_index + 1

            end_time = start_time + processing_time

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine load and job completion time
            machine_load[machine] = end_time
            job_completion_times[job] = end_time
            eligible_operations[job] += 1
            scheduled_operations += 1

    return schedule
