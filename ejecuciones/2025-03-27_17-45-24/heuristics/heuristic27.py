
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that considers machine load
    and operation precedence to minimize makespan and balance machine workload.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Completion time of each job

    # Sort jobs by the sum of their processing times (shortest job first)
    job_priorities = sorted(jobs.keys(), key=lambda job: sum(min(times) for machines, times in jobs[job]))

    for job in job_priorities:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Find the machine that can start the operation earliest, considering both machine availability and job completion time
            best_machine = None
            earliest_start_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_time = times[machine_idx]  # Corresponding processing time

            # Assign the operation to the best machine
            start_time = earliest_start_time
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
