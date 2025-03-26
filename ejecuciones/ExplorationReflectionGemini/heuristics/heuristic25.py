
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time on machines
    and job completion time by selecting the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None
            
            # Iterate through possible machines for the current operation
            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]

                # Calculate the earliest possible start time on this machine
                start_time = max(machine_available_time[machine], job_completion_time[job])

                # Check if this machine offers a better start time
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Assign the operation to the best machine found
            start_time = best_start_time
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
