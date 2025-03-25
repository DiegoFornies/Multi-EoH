
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time on machines
    and operation completion time, selecting the machine that results in the
    earliest operation end time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize machine availability times and job completion times
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Initialize the schedule
    schedule = {}

    # Iterate through each job
    for job_id, operations in jobs_data.items():
        schedule[job_id] = []
        # Iterate through each operation in the job
        for op_idx, (machines, times) in enumerate(operations):
            op_num = op_idx + 1

            # Find the machine that allows the earliest completion time
            best_machine, best_start_time, best_end_time, best_processing_time = None, float('inf'), float('inf'), None
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < best_end_time:
                    best_machine, best_start_time, best_end_time, best_processing_time = machine, start_time, end_time, processing_time

            # Assign the operation to the best machine
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability time and job completion time
            machine_available_time[best_machine] = best_end_time
            job_completion_time[job_id] = best_end_time

    return schedule
