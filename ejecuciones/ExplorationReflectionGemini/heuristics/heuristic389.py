
def heuristic(input_data):
    """Schedules jobs using a combination of SPT and load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
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
                if op_idx == 0 or ((job, op_idx - 1) in scheduled_ops and job_completion_time[job] > 0):
                    eligible_operations.append((job, op_idx, machines, times))

        if not eligible_operations:
            break

        best_op = None
        best_machine = None
        earliest_start_time = float('inf')
        shortest_processing_time = float('inf')

        for job, op_idx, machines, times in eligible_operations:
            available_machines = []
            for idx, machine in enumerate(machines):
                available_machines.append((machine, times[idx]))
            
            best_available_time = float('inf')
            best_available_machine = None
            processing_time_candidate = float('inf')

            for m, t in available_machines:
                start_time = max(machine_time[m], job_completion_time[job])
                if start_time < best_available_time:
                    best_available_time = start_time
                    best_available_machine = m
                    processing_time_candidate = t

            if best_available_time < earliest_start_time or (best_available_time == earliest_start_time and processing_time_candidate < shortest_processing_time):
                earliest_start_time = best_available_time
                shortest_processing_time = processing_time_candidate
                best_op = (job, op_idx, machines, times)
                best_machine = best_available_machine

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
            scheduled_ops.add((job, op_idx))

    return schedule
