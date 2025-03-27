
def heuristic(input_data):
    """
    Heuristic scheduling for FJSSP: Prioritizes shortest processing time
    and earliest available machine for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        ops = jobs_data[job_id]

        for op_idx, (machines, times) in enumerate(ops):
            op_num = op_idx + 1

            # Find the machine with the earliest available time and shortest processing time
            best_machine, best_time = None, float('inf')
            for m_idx, machine in enumerate(machines):
                if times[m_idx] < best_time:
                    if max(machine_available_time[machine], job_completion_time[job_id]) + times[m_idx] < float('inf'):
                        best_machine = machine
                        best_time = times[m_idx]

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
    return schedule
