
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with the fewest feasible machines
    and assigns them to the machine with the earliest available time, balancing
    machine load and minimizing makespan.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule, machine availability, and job completion times
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    operation_queue = []
    
    # Populate initial operation queue sorted by number of available machine and jobs
    for job, operations in jobs_data.items():
        operation_queue.append((job, 0))

    scheduled_operations = {}
    
    while operation_queue:
        # Sort the queue and get operation with the fewest number of possible machines for scheduling
        operation_queue = sorted(operation_queue, key=lambda x: len(jobs_data[x[0]][x[1]][0]))
        job, op_idx = operation_queue.pop(0)
        machines, times = jobs_data[job][op_idx]
        op_num = op_idx + 1

        # Find the machine with the earliest available time among feasible machines
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for m_idx, m in enumerate(machines):
            start_time = max(machine_available_time[m], job_completion_time[job])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = times[m_idx]

        # Schedule the operation on the selected machine
        start = best_start_time
        end = start + best_processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start,
            'End Time': end,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = end
        job_completion_time[job] = end

        # Add the next operation of the job to the queue, if any
        if op_idx + 1 < len(jobs_data[job]):
            operation_queue.append((job, op_idx + 1))
            
    return schedule
