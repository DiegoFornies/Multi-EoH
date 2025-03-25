
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes jobs with fewer operations
    and assigns operations to machines with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Sort jobs based on the number of operations (shortest job first)
    job_order = sorted(jobs_data.keys(), key=lambda job: len(jobs_data[job]))

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data.keys()}
    schedule = {job: [] for job in jobs_data.keys()}

    for job in job_order:
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_available_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                available_time = max(machine_available_time[machine], job_completion_time[job])

                if available_time < min_available_time:
                    min_available_time = available_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the selected machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
