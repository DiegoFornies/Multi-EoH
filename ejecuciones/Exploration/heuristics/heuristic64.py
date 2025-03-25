
def heuristic(input_data):
    """Combines earliest start time and machine load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []

    remaining_ops = {}
    for job_id, operations in jobs.items():
        remaining_ops[job_id] = list(range(len(operations)))

    scheduled_count = 0
    total_ops = sum(len(ops) for ops in jobs.values())

    while scheduled_count < total_ops:
        eligible_operations = []
        for job_id, ops in jobs.items():
            if remaining_ops[job_id]:
                op_idx = remaining_ops[job_id][0]
                eligible_operations.append((job_id, op_idx))

        best_op = None
        best_machine = None
        earliest_start = float('inf')
        lowest_load = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs[job_id][op_idx]

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < earliest_start:
                    earliest_start = start_time
                    lowest_load = machine_load[machine]
                    best_op = (job_id, op_idx)
                    best_machine = (machine, m_idx)
                elif start_time == earliest_start and machine_load[machine] < lowest_load:
                    lowest_load = machine_load[machine]
                    best_op = (job_id, op_idx)
                    best_machine = (machine, m_idx)


        if best_op is not None:
            job_id, op_idx = best_op
            machine, time_idx = best_machine
            machines, times = jobs[job_id][op_idx]
            processing_time = times[time_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[machine] += processing_time
            remaining_ops[job_id].pop(0)
            scheduled_count += 1

    return schedule
