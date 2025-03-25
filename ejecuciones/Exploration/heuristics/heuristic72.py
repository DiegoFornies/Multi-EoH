
def heuristic(input_data):
    """Combines earliest available time, job priority, and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    
    for job_id in jobs:
        schedule[job_id] = []

    remaining_operations = {job: list(range(len(ops))) for job, ops in jobs.items()}
    job_priority = sorted(jobs.keys(), key=lambda job: len(remaining_operations[job]), reverse=True)

    scheduled_count = 0
    total_ops = sum(len(ops) for ops in jobs.values())

    while scheduled_count < total_ops:
        eligible_operations = []
        for job in job_priority:
            if remaining_operations[job]:
                op_idx = remaining_operations[job][0]
                eligible_operations.append((job, op_idx, job))

        best_op = None
        best_machine = None
        earliest_start = float('inf')
        least_loaded_machine = float('inf')

        for op_idx, job, job_id in [(op_idx, job, job_id) for op_idx, (job_id, op_idx) in enumerate([(op_idx, job_id) for job_id, op_idx in [(job_id, op_idx) for job_id, ops in jobs.items() if remaining_operations[job_id] for op_idx in [remaining_operations[job_id][0]]] ], job in [job_id for job_id, ops in jobs.items() if remaining_operations[job_id]])]:
            machines, times = jobs[job][job_id]
            
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_end_time[job])
                end_time = start_time + times[m_idx]
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = (job, job_id)
                    best_machine = (machine, m_idx)
        if best_op is not None:

            job, op_idx = best_op
            machine, time_idx = best_machine
            machines, times = jobs[job][op_idx]
            processing_time = times[time_idx]
            start_time = max(machine_available_time[machine], job_end_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            machine_available_time[machine] = end_time
            job_end_time[job] = end_time
            machine_load[machine] += processing_time
            remaining_operations[job].pop(0)
            scheduled_count += 1

    return schedule
