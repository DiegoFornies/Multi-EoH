
def heuristic(input_data):
    """
    Aims to minimize makespan using a greedy approach with machine load balancing.
    Schedules operations on the least loaded available machine.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    for job in jobs:
        schedule[job] = []

    for job in jobs:
        op_idx = 0
        while op_idx < len(jobs[job]):
            machines, times = jobs[job][op_idx]
            operation_number = op_idx + 1

            # Find the earliest available time slot among feasible machines
            best_machine = -1
            min_start_time = float('inf')
            processing_time = -1

            for machine_index in range(len(machines)):
                machine = machines[machine_index]
                time = times[machine_index]

                start_time = max(machine_available_time[machine], job_completion_time[job])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    processing_time = time

            # Schedule the operation on the selected machine
            start_time = min_start_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

            op_idx += 1

    return schedule
