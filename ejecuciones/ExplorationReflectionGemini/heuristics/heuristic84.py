
def heuristic(input_data):
    """Combines machine load and SPT for FJSSP."""
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
        earliest_end_time = float('inf')

        for job, op_idx, machines, times in eligible_operations:
            best_local_machine = None
            min_local_time = float('inf')
            least_loaded_machine = None
            min_load = float('inf')

            for m in machines:
                if machine_load[m] < min_load:
                    min_load = machine_load[m]
                    least_loaded_machine = m

            for idx, machine in enumerate(machines):
                processing_time = times[idx]
                if machine == least_loaded_machine:
                    start_time = max(machine_time[machine], job_completion_time[job])
                    end_time = start_time + processing_time
                    if end_time < min_local_time:
                        min_local_time = end_time
                        best_local_machine = machine

            if best_local_machine is not None:
                local_processing_time = times[machines.index(best_local_machine)]
                local_start_time = max(machine_time[best_local_machine], job_completion_time[job])
                local_end_time = local_start_time + local_processing_time
                if local_end_time < earliest_end_time:
                    earliest_end_time = local_end_time
                    best_op = (job, op_idx, machines, times)
                    best_machine = best_local_machine

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
