
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shorter operations and balances machine load.
    Chooses the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort jobs based on the total processing time of their operations.
    job_order = sorted(jobs_data.keys(), key=lambda job_id: sum(min(times) for machines, times in jobs_data[job_id]))

    for job in job_order:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            
            # Find the machine with the earliest available time among feasible machines.
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                elif start_time == min_start_time and processing_time < best_processing_time :
                    best_machine = machine
                    best_processing_time = processing_time
            
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
