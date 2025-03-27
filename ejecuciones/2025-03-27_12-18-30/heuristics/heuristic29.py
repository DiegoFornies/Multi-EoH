
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that considers both machine availability and operation processing time.
    Prioritizes operations based on shortest processing time among feasible machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}  # Store the schedule for each job
    machine_available_time = {m: 0 for m in range(n_machines)}  # Track when each machine becomes available
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Track when each job completes its previous operation

    # Initialize the schedule for each job
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # List of operations, (job_id, op_index), to be scheduled
    operations_to_schedule = []
    for job_id, operations in jobs.items():
        for op_index in range(len(operations)):
            operations_to_schedule.append((job_id, op_index))

    while operations_to_schedule:
        # Find the best operation to schedule based on earliest end time.
        best_operation = None
        earliest_end_time = float('inf')

        for job_id, op_index in operations_to_schedule:
            machines, times = jobs[job_id][op_index]

            # Find the machine that gives the earliest completion time for this operation
            best_machine_for_op = None
            earliest_completion_time_for_op = float('inf')
            processing_time = None

            for m_index, m in enumerate(machines):
                available_time = machine_available_time[m]
                start_time = max(available_time, job_completion_time[job_id])
                end_time = start_time + times[m_index]

                if end_time < earliest_completion_time_for_op:
                    earliest_completion_time_for_op = end_time
                    best_machine_for_op = m
                    processing_time = times[m_index]
                    start_time_selected = start_time

            if earliest_completion_time_for_op < earliest_end_time:
                earliest_end_time = earliest_completion_time_for_op
                best_operation = (job_id, op_index, best_machine_for_op, processing_time, start_time_selected)
        
        # Schedule the best operation
        job_id, op_index, assigned_machine, processing_time, start_time = best_operation
        op_num = op_index + 1
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine available time and job completion time
        machine_available_time[assigned_machine] = end_time
        job_completion_time[job_id] = end_time

        # Remove the scheduled operation from the list
        operations_to_schedule.remove((job_id, op_index))
    return schedule
