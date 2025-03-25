
def heuristic(input_data):
    """A heuristic for the Flexible Job Shop Scheduling Problem that prioritizes machine utilization and minimizes idle time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine availability times
    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}

    # Prioritize operations based on shortest processing time (SPT) among available machines.
    operation_queue = []
    for job_id, operations in jobs.items():
        schedule[job_id] = []
        operation_queue.append((job_id, 0))  # (job_id, operation_index)

    # Schedule operations until all jobs are completed
    while operation_queue:
        best_job, best_op_idx = None, None
        min_end_time = float('inf')
        best_machine = None
        best_processing_time = None

        # Find the next operation to schedule that minimizes completion time
        for job_id, op_idx in operation_queue:
            available_machines, processing_times = jobs[job_id][op_idx]

            # Find the machine that allows for the earliest completion time
            for machine_idx, machine in enumerate(available_machines):
                processing_time = processing_times[machine_idx]

                # Calculate start time considering machine and job constraints
                job_completion_time = 0
                for scheduled_op in schedule[job_id]:
                    job_completion_time = max(job_completion_time, scheduled_op['End Time'])

                start_time = max(machine_availability[machine], job_completion_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_job = job_id
                    best_op_idx = op_idx
                    best_machine = machine
                    best_processing_time = processing_time

        # Schedule the operation on the selected machine
        start_time = 0
        for scheduled_op in schedule[best_job]:
            start_time = max(start_time, scheduled_op['End Time'])

        start_time = max(start_time, machine_availability[best_machine])
        end_time = start_time + best_processing_time

        schedule[best_job].append({
            'Operation': best_op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability time
        machine_availability[best_machine] = end_time

        # Add the next operation of the job to the queue
        operation_queue.remove((best_job, best_op_idx))
        if best_op_idx + 1 < len(jobs[best_job]):
            operation_queue.append((best_job, best_op_idx + 1))

    return schedule
