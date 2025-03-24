
def heuristic(input_data):
    """Schedules jobs, minimizing makespan and balancing machine load."""
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

            # Find the machine with the least load among available machines
            best_machine = None
            min_end_time = float('inf')
            best_time = None

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                start_time = max(machine_load[machine], job_completion_times[job])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_time = time

            # Schedule the operation on the selected machine
            start_time = max(machine_load[best_machine], job_completion_times[job])
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine load and job completion time
            machine_load[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
