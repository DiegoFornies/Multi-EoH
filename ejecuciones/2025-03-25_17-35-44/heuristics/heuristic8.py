
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem that prioritizes
    jobs with the most operations and assigns operations to the least loaded
    machine among the available options.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Sort jobs by number of operations in descending order
    job_priority = sorted(jobs.items(), key=lambda item: len(item[1]), reverse=True)

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_finish_time = {job: 0 for job in jobs}

    for job, operations in job_priority:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(operations):
            op_num = op_idx + 1

            # Find the least loaded machine among available machines
            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_finish_time[job])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_time = times[i]

            # Schedule the operation on the best machine
            start_time = max(machine_time[best_machine], job_finish_time[job])
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine and job finish times
            machine_time[best_machine] = end_time
            job_finish_time[job] = end_time

    return schedule
