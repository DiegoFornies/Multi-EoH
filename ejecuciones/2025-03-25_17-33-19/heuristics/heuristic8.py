
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules operations greedily, prioritizing
    the shortest processing time on the least loaded machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job in jobs_data:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation
            op_num = op_idx + 1
            
            # Find the machine with the earliest available time and shortest processing time
            best_machine, best_time = None, float('inf')
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                available_time = max(machine_load[machine], job_completion_times[job])

                if available_time + time < best_time:
                    best_machine = machine
                    best_time = available_time + time
                    processing_time = time
                    selected_time = time

            start_time = max(machine_load[best_machine], job_completion_times[job])
            end_time = start_time + selected_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': selected_time
            })

            machine_load[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
