
def heuristic(input_data):
    """Schedules jobs based on shortest processing time and earliest available machine, considering job sequencing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}  # Store the final schedule
    machine_available_time = {m: 0 for m in range(n_machines)}  # Track when each machine is available
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Track when each job's previous operation finished

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []  # Initialize schedule for each job

    # Flatten operations across all jobs into a list of tuples (job_id, operation_index, operation_details)
    operations = []
    for job_id, ops in jobs.items():
        for op_idx, op_details in enumerate(ops):
            operations.append((job_id, op_idx + 1, op_details))
    
    # Sort operations based on shortest processing time heuristic
    operations.sort(key=lambda op: min(op[2][1]))  # Prioritize ops with shortest possible processing time


    for job_id, op_num, op_details in operations:
        machines, times = op_details

        # Find the machine and time that allows the operation to start the earliest, respecting job sequencing
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the selected machine
        end_time = best_start_time + best_processing_time
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
