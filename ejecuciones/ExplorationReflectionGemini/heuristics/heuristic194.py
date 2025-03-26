
def heuristic(input_data):
    """Dynamic priority, reacting to real-time scheduling conditions."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times, job))

    scheduled_ops = set()

    while len(scheduled_ops) < len(operations):
        eligible_operations = []
        for job, op_idx, machines, times, original_job in operations:
            if (job, op_idx, original_job) not in scheduled_ops:
                if op_idx == 0 or ((job, op_idx - 1, original_job) in scheduled_ops and job_completion_time[original_job] > 0):
                    eligible_operations.append((job, op_idx, machines, times, original_job))

        if not eligible_operations:
            break

        best_op = None
        best_machine = None
        best_priority = float('inf')

        for job, op_idx, machines, times, original_job in eligible_operations:
            available_machines = []
            for idx, machine in enumerate(machines):
                available_machines.append((machine, times[idx], machine))

            for processing_time, machine in [(time, mach) for time, mach, mach_ in available_machines]:

                start_time = max(machine_time[machine], job_completion_time[original_job])

                # Dynamic priority based on machine load and remaining job time
                priority = start_time + (sum([min(t) for _, (m, t) in jobs.items() if m == original_job])) # Remaining time approximation

                if priority < best_priority:
                    best_priority = priority
                    best_op = (job, op_idx, machines, times, original_job)
                    best_machine = machine
                    best_processing_time = processing_time

        if best_op is not None:
            job, op_idx, machines, times, original_job = best_op
            op_num = op_idx + 1

            start_time = max(machine_time[best_machine], job_completion_time[original_job])
            end_time = start_time + best_processing_time

            if original_job not in schedule:
                schedule[original_job] = []

            schedule[original_job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[original_job] = end_time
            scheduled_ops.add((job, op_idx, original_job))

    return schedule
