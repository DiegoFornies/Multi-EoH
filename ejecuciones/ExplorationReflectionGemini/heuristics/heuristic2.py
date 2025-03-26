
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that considers both machine availability and operation processing time
    when assigning operations to machines to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Iterate through jobs and operations
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine that minimizes the operation's completion time
            best_machine = None
            min_completion_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            # Assign the operation to the best machine
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_completion_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = min_completion_time
            job_completion_time[job] = min_completion_time

    return schedule
