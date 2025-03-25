
def heuristic(input_data):
    """
    A heuristic for FJSSP prioritizing jobs with fewer remaining operations
    and machines with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize machine availability times
    machine_available_time = {m: 0 for m in range(n_machines)}
    # Store job-specific operation details to schedule
    job_operations = {job: [(idx + 1, op) for idx, op in enumerate(ops)] for job, ops in jobs_data.items()}

    schedule = {}  # Store the final schedule
    for job in jobs_data.keys():
        schedule[job] = []

    scheduled_operations = set()  # Operations already scheduled, avoids duplication

    # Helper function to find the earliest available machine and start time for an operation
    def find_earliest_machine(machines, times):
        """Finds the machine with the earliest available time for the op."""
        earliest_machine, earliest_time, earliest_start = None, float('inf'), None
        for m, t in zip(machines, times):
            start_time = max(machine_available_time[m], 0)
            if start_time < earliest_time:
                earliest_time = start_time
                earliest_machine = m
                earliest_start = start_time
        return earliest_machine, earliest_start

    # Iterate while there are unscheduled operations
    while True:
        available_operations = []

        # Find available operations (first operation of any job not yet scheduled)
        for job in jobs_data.keys():
            if job in job_operations and job_operations[job]:
                op_num, (machines, times) = job_operations[job][0]
                available_operations.append((job, op_num, machines, times))
        
        if not available_operations:
            break  # No more operations to schedule

        # Prioritize jobs with fewer remaining operations (Shortest Queue First)
        available_operations.sort(key=lambda x: len(job_operations[x[0]]))

        # Select the best operation based on the heuristic criteria
        best_operation = None
        earliest_start_overall = float('inf')
        best_machine = None

        for job, op_num, machines, times in available_operations:
            machine, start_time = find_earliest_machine(machines, times)
            if start_time < earliest_start_overall:
                earliest_start_overall = start_time
                best_operation = (job, op_num, machines, times)
                best_machine = machine
        
        # Schedule the best operation
        job, op_num, machines, times = best_operation
        processing_time = times[machines.index(best_machine)]
        start_time = earliest_start_overall
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability
        machine_available_time[best_machine] = end_time

        # Remove scheduled operation from available operations of the job
        job_operations[job].pop(0)
        if not job_operations[job]:
            del job_operations[job]  # If job completed, remove its operations
    
    return schedule
