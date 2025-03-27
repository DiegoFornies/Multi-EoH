
def heuristic(input_data):
    """
    A heuristic for FJSSP that aims to minimize makespan by considering
    both machine availability and operation processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine availability
    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Iterate through each job
    for job_id, operations in jobs.items():
        schedule[job_id] = []

        # Iterate through each operation in the job
        for op_idx, operation in enumerate(operations):
            machines, processing_times = operation

            # Find the earliest available machine and its start time
            best_machine = None
            earliest_start = float('inf')
            processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                time = processing_times[i]
                start_time = max(machine_availability[machine], job_completion_times[job_id])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine
                    processing_time = time
            
            # Assign the operation to the best machine and update schedules
            start_time = earliest_start
            end_time = start_time + processing_time
            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine availability and job completion time
            machine_availability[best_machine] = end_time
            job_completion_times[job_id] = end_time
    return schedule
