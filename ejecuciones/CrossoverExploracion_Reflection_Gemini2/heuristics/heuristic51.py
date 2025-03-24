
def heuristic(input_data):
    """Schedules jobs, minimizing makespan by selecting machines with earliest completion times."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        operations = jobs_data[job]
        for op_idx, operation in enumerate(operations):
            machines, times = operation

            best_machine = -1
            min_completion_time = float('inf')
            best_time = 0
            best_start_time = 0

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                completion_time = start_time + time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_time = time
                    best_start_time = start_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_completion_time,
                'Processing Time': best_time
            })

            machine_available_time[best_machine] = min_completion_time
            job_completion_time[job] = min_completion_time

    return schedule
