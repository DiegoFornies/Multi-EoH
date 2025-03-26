
def heuristic(input_data):
    """Schedules jobs using combined earliest start and load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

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
        min_weighted_time = float('inf')

        for job, op_idx, machines, times in eligible_operations:
            for idx, machine in enumerate(machines):
                processing_time = times[idx]
                start_time = max(machine_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                # Weighted time considers start time, processing time, and machine load
                weighted_time = start_time + processing_time + 0.05 * machine_load[machine]  # Adjusted weight

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
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
            machine_load[best_machine] += processing_time
            job_completion_time[job] = end_time
            scheduled_ops.add((job, op_idx))

    return schedule
