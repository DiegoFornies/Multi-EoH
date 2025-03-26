
def heuristic(input_data):
    """Combines SPT, load balancing, and operation urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}
    job_remaining_work = {j: sum(min(t) for _, t in ops) for j, ops in jobs.items()}

    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    operations.sort(key=lambda x: (x[0], x[1]))
    scheduled_ops = set()

    while len(scheduled_ops) < len(operations):
        eligible_operations = []
        for job, op_idx, machines, times in operations:
            if (job, op_idx) not in scheduled_ops:
                if op_idx == 0 or ((job, op_idx - 1) in scheduled_ops and
                                    job_completion_time[job] > 0):
                    eligible_operations.append((job, op_idx, machines, times))

        if not eligible_operations:
            break

        best_op = None
        best_machine = None
        best_priority = float('inf')

        for job, op_idx, machines, times in eligible_operations:
            available_machines = []
            for idx, machine in enumerate(machines):
                available_machines.append((machine, machine, times[idx]))

            for m, machine, t in available_machines:
                start_time = max(machine_time[machine], job_completion_time[job])
                # Urgency factor: prioritize jobs with less remaining work
                urgency = job_remaining_work[job] / (1 + start_time)
                # Load balance factor: favor machines with lower utilization
                load_balance = machine_time[machine]

                priority = start_time + 0.1 * load_balance - 0.05 * urgency

                if priority < best_priority:
                    best_priority = priority
                    best_op = (job, op_idx, machines, times)
                    best_machine = machine

        if best_op is not None:
            job, op_idx, machines, times = best_op
            op_num = op_idx + 1
            processing_time = times[machines.index(best_machine)]
            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time
            job_remaining_work[job] -= processing_time
            scheduled_ops.add((job, op_idx))

    return schedule
