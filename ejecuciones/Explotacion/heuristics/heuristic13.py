
def heuristic(input_data):
    """Combines least load and shortest processing time for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {machine: 0 for machine in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        operations = jobs[job]
        for op_idx, op_data in enumerate(operations):
            machines, times = op_data

            best_machine = None
            min_end_time = float('inf')
            best_time = float('inf')
            
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                start_time = max(machine_load[machine], job_completion_times[job])
                end_time = start_time + time

                if end_time < min_end_time or (end_time == min_end_time and time < best_time):
                    min_end_time = end_time
                    best_machine = machine
                    best_time = time

            start_time = max(machine_load[best_machine], job_completion_times[job])
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_load[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
