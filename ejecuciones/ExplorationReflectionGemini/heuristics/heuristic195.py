
def heuristic(input_data):
    """Schedules jobs adaptively considering machine load and job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times, job))

    operations.sort(key=lambda x: (x[4], x[1]))

    scheduled_ops = set()

    while len(scheduled_ops) < len(operations):
        eligible_operations = []
        for job, op_idx, machines, times, original_job in operations:
            if (job, op_idx) not in scheduled_ops:
                if op_idx == 0 or ((job, op_idx - 1) in scheduled_ops and job_completion_time[original_job] > 0):
                    eligible_operations.append((job, op_idx, machines, times, original_job))

        if not eligible_operations:
            break

        best_op = None
        best_machine = None
        best_start_time = float('inf')

        for job, op_idx, machines, times, original_job in eligible_operations:
            available_machines = []
            for idx, machine in enumerate(machines):
                available_machines.append((machine, times[idx]))

            best_available_time = float('inf')
            best_available_machine = None

            for m, t in available_machines:
                start_time = max(machine_time[m], job_completion_time[original_job])
                load_factor = machine_load[m]
                combined_metric = start_time + 0.1 * load_factor # Dynamic adjustment might be necessary based on problem scale
                if combined_metric < best_available_time:
                    best_available_time = combined_metric
                    best_available_machine = m
                    
            if best_available_time < best_start_time:
                    best_start_time = best_available_time
                    best_op = (job, op_idx, machines, times, original_job)
                    best_machine = best_available_machine

        if best_op is not None:
            job, op_idx, machines, times, original_job = best_op
            op_num = op_idx + 1
            processing_time = times[machines.index(best_machine)]

            start_time = max(machine_time[best_machine], job_completion_time[original_job])
            end_time = start_time + processing_time

            if original_job not in schedule:
                schedule[original_job] = []

            schedule[original_job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time[original_job] = end_time
            scheduled_ops.add((job, op_idx))

    return schedule
