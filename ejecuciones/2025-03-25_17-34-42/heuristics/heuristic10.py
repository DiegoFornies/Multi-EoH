
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) 
    that minimizes makespan by prioritizing operations based on 
    shortest processing time among available machines and earliest
    machine available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    job_operations = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}

    # Maintain a list of ready operations for each job
    ready_operations = {job: [] for job in range(1, n_jobs + 1)}
    for job in range(1, n_jobs + 1):
        ready_operations[job].append(1)  # Start with the first operation ready

    completed_operations = {job: [] for job in range(1, n_jobs + 1)}

    while any(ready_operations.values()):
        # Find the next best operation to schedule
        best_job, best_op, best_machine, best_start, best_processing_time = None, None, None, float('inf'), None

        for job in range(1, n_jobs + 1):
            if not ready_operations[job]:
                continue

            op_index = ready_operations[job][0] - 1
            machines, times = jobs_data[job][op_index]

            # Find the machine that provides the shortest processing time
            for m_index, machine in enumerate(machines):
                processing_time = times[m_index]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                # Choose the machine that results in the earliest completion time
                if start_time < best_start:
                    best_job, best_op, best_machine, best_start, best_processing_time = job, op_index + 1, machine, start_time, processing_time

        # Schedule the best operation
        if best_job is not None:
            schedule[best_job].append({
                'Operation': best_op,
                'Assigned Machine': best_machine,
                'Start Time': best_start,
                'End Time': best_start + best_processing_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job times
            machine_available_time[best_machine] = best_start + best_processing_time
            job_completion_time[best_job] = best_start + best_processing_time

            # Mark operation as complete and update ready operations
            completed_operations[best_job].append(best_op)
            ready_operations[best_job].pop(0)  # Remove current ready operation

            # Make the next operation ready if it exists
            if best_op < len(jobs_data[best_job]):
                next_op = best_op + 1
                ready_operations[best_job].append(next_op)

    return schedule
