
def heuristic(input_data):
    """
    A heuristic for the FJSSP that minimizes makespan by considering machine load
    and job precedence. It prioritizes operations based on processing time and
    machine availability to balance machine load and reduce idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    
    # Create a list of operations, each represented as a tuple:
    # (job_id, operation_index, list of possible machines, list of processing times)
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations based on shortest processing time on the fastest available machine, then by job
    operations.sort(key=lambda op: min(op[3]), reverse = False)

    # Process operations one by one
    while operations:
        best_op = None
        best_machine = None
        earliest_start_time = float('inf')

        for op_idx, (job_id, op_num, machines, times) in enumerate(operations):
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                available_time = machine_available_time[machine]
                job_ready_time = job_completion_time[job_id]

                start_time = max(available_time, job_ready_time)
                
                # Select the earliest available machine
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_op = (job_id, op_num, machines, times)
                    best_op_index = op_idx

        # Schedule the operation on the selected machine
        job_id, op_num, machines, times = best_op
        machine_idx = machines.index(best_machine)
        processing_time = times[machine_idx]

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        # Remove the scheduled operation from the list of operations
        del operations[best_op_index]

    return schedule
