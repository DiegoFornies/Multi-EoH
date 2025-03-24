
def heuristic(input_data):
    """
    A dispatching rule-based heuristic for the FJSSP,
    prioritizing shortest processing time (SPT) within eligible machines.
    Also considers machine idle time to minimize makespan.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine availability
    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)} #Job number starts from 1

    # Create a list of operations, sorted by job
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op_data)) # job_id, operation number, (machines, times)

    # Sort operations based on the shortest processing time on the fastest eligible machine
    operations.sort(key=lambda x: min(x[2][1])) #prioritize shortest processing time

    # Process each operation
    for job_id, op_num, op_data in operations:
        machines, times = op_data

        # Find the machine with the earliest availability among the eligible machines
        best_machine = None
        min_start_time = float('inf')
        
        for i, machine in enumerate(machines):
            start_time = max(machine_availability[machine], job_completion_times[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_time_index = i # track the index for processing time retrieval

        # Schedule the operation on the selected machine
        start_time = max(machine_availability[best_machine], job_completion_times[job_id])
        processing_time = times[best_time_index]
        end_time = start_time + processing_time

        # Update machine availability and job completion time
        machine_availability[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Add the operation to the schedule
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

    return schedule
