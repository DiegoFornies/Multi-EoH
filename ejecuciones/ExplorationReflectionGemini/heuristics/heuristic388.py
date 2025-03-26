
def heuristic(input_data):
    """FJSSP Heuristic: Combines load balancing, SPT, and job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_remaining_times = {}

    for job_id in range(1, n_jobs + 1):
        remaining_time = 0
        for machines, times in jobs[job_id]:
            remaining_time += min(times)
        job_remaining_times[job_id] = remaining_time

    operations = []
    for job_id, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job_id, op_idx, machines, times))

    operations.sort(key=lambda x: (x[0], x[1]))

    scheduled_ops = set()

    while len(scheduled_ops) < len(operations):
        eligible_operations = []
        for job_id, op_idx, machines, times in operations:
            if (job_id, op_idx) not in scheduled_ops:
                if op_idx == 0 or ((job_id, op_idx - 1) in scheduled_ops and
                                    job_completion_time[job_id] > 0):
                    eligible_operations.append((job_id, op_idx, machines, times))

        if not eligible_operations:
            break

        best_op = None
        best_machine = None
        min_cost = float('inf')

        for job_id, op_idx, machines, times in eligible_operations:
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                cost = processing_time + 0.1 * machine_load[machine] + start_time * 0.01 - 0.05 * job_remaining_times[job_id]

                if cost < min_cost:
                    min_cost = cost
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
                    best_job_id = job_id
                    best_op_idx = op_idx

        if best_machine is not None:

            machine_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[best_job_id] = best_start_time + best_processing_time
            job_remaining_times[best_job_id] -= best_processing_time
            scheduled_ops.add((best_job_id, best_op_idx))

            schedule[best_job_id].append({
                'Operation': best_op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
