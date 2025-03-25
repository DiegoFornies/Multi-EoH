
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing makespan 
    by selecting the machine with the earliest available time
    for each operation.
    """
    schedule, machine_time = {}, {m: 0 for m in range(input_data['n_machines'])}
    job_time = {job: 0 for job in input_data['jobs']}  # Track completion time of each job

    for job, ops in input_data['jobs'].items():
        schedule[job] = []

        for op_idx, (machines, times) in enumerate(ops):
            op_num = op_idx + 1

            # Find the machine with the earliest available time
            best_machine, best_time, best_processing_time = None, float('inf'), None
            for i, m in enumerate(machines):
                available_time = max(machine_time[m], job_time[job])
                if available_time < best_time:
                    best_time = available_time
                    best_machine = m
                    best_processing_time = times[i]

            start = best_time
            end = start + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start,
                'End Time': end,
                'Processing Time': best_processing_time
            })

            machine_time[best_machine] = end
            job_time[job] = end

    return schedule
