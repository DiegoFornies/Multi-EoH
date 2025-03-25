
def heuristic(input_data):
    """Schedules jobs using SPT and load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_priority = {}
    for job_id in range(1, n_jobs + 1):
        job_priority[job_id] = len(jobs[job_id])
    available_operations = []
    for job_id in jobs:
        available_operations.append((job_id, 1))
    while available_operations:
        best_op = None
        min_end_time = float('inf')
        for job_id, op_num in available_operations:
            machines, times = jobs[job_id][op_num - 1]
            earliest_start_time = float('-inf')
            chosen_machine = None
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], (schedule[job_id][-1]['End Time'] if job_id in schedule and schedule[job_id] else 0)) if op_num > 1 else machine_available_times[m]
                end_time = start_time + times[m_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    earliest_start_time = start_time
                    best_op = (job_id, op_num, m, times[m_idx])
                elif end_time == min_end_time:
                    if machine_load[m] < machine_load[chosen_machine if chosen_machine is not None else machines[0]]:
                        best_op = (job_id, op_num, m, times[m_idx])
                        earliest_start_time = start_time
                        chosen_machine = m
        if best_op is None:
            break

        job_id, op_num, assigned_machine, processing_time = best_op
        start_time = max(machine_available_times[assigned_machine], (schedule[job_id][-1]['End Time'] if job_id in schedule and schedule[job_id] else 0)) if op_num > 1 else machine_available_times[assigned_machine]
        end_time = start_time + processing_time
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({'Operation': op_num, 'Assigned Machine': assigned_machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': processing_time})
        machine_available_times[assigned_machine] = end_time
        machine_load[assigned_machine] += processing_time
        available_operations.remove((job_id, op_num))
        if op_num < len(jobs[job_id]):
            available_operations.append((job_id, op_num + 1))
    return schedule
