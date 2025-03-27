
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes jobs with fewer operations
    and machines with the earliest available time.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    # Sort jobs by number of operations
    job_order = sorted(jobs_data.keys(), key=lambda job: len(jobs_data[job]))

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data.keys()}

    for job in job_order:
        schedule[job] = []
        ops = jobs_data[job]

        for op_idx, (machines, times) in enumerate(ops):
            op_num = op_idx + 1

            # Find the machine with the earliest available time from the available machines for this operation
            best_machine = None
            min_available_time = float('inf')
            
            for m in machines:
                if machine_available_time[m] < min_available_time:
                    min_available_time = machine_available_time[m]
                    best_machine = m

            # Get corresponding processing time
            machine_index = machines.index(best_machine)
            processing_time = times[machine_index]

            # Calculate start and end times, considering both machine and job completion times
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            # Update the schedule, machine availability, and job completion time
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
