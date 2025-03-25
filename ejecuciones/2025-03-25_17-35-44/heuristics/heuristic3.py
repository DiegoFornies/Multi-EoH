
def heuristic(input_data):
    """
    A dispatching rule-based heuristic for FJSSP, prioritizing operations
    with the shortest processing time on the least loaded machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    scheduled_operations = {}

    # Create a list of unscheduled operations with job and operation number
    unscheduled_operations = []
    for job, operations in jobs.items():
        for op_idx, op_data in enumerate(operations):
            unscheduled_operations.append((job, op_idx + 1))

    while unscheduled_operations:
        # Find the best operation based on the heuristic
        best_operation = None
        min_makespan = float('inf')

        for job, op_num in unscheduled_operations:
            op_idx = op_num - 1
            machines, times = jobs[job][op_idx]

            # Evaluate each machine option for the current operation
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                # Consider makespan (completion time) when choosing best operation
                makespan = end_time

                if makespan < min_makespan:
                    min_makespan = makespan
                    best_operation = (job, op_num, machine, processing_time, start_time, end_time)

        # Schedule the best operation
        job, op_num, assigned_machine, processing_time, start_time, end_time = best_operation
        op_idx = op_num - 1

        if job not in scheduled_operations:
            scheduled_operations[job] = []

        scheduled_operations[job].append({
            'Operation': op_num,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[assigned_machine] = end_time
        job_completion_time[job] = end_time

        # Remove the scheduled operation from the unscheduled list
        unscheduled_operations.remove((job, op_num))

    return scheduled_operations
