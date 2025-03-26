
def heuristic(input_data):
    """Combines makespan and load balancing for FJSSP."""
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
            available_machines = []
            for idx, machine in enumerate(machines):
                available_machines.append((machine, times[idx]))

            for m, t in available_machines:
                start_time = max(machine_time[m], job_completion_time[job])
                end_time = start_time + t
                weighted_time = end_time + 0.01 * machine_load[m]

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_op = (job, op_idx, machines, times)
                    best_machine = m
                    best_start_time = start_time
                    best_processing_time = t

        if best_op is not None:
            job, op_idx, machines, times = best_op
            op_num = op_idx + 1

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time
            scheduled_ops.add((job, op_idx))

    return schedule
