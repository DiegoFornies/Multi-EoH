
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations based on shortest processing time on least loaded machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    scheduled_operations = {}

    # Create a list of all operations, sorted by job and operation number
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    #Sort by earliest jobs
    operations.sort(key=lambda x: x[0])
    
    schedule = {}
    for job_id in jobs_data.keys():
        schedule[job_id] = []
    
    while operations:
        # Find the next operation to schedule
        best_op = None
        best_machine = None
        min_end_time = float('inf')
        
        for job_id, op_num, machines, times in operations:
            available_machines = []
            for i in range(len(machines)):
                available_machines.append((machines[i], times[i]))

            #Find the machine that will finish operations the earliest
            for machine, time in available_machines:
                start_time = max(machine_load[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_num, machines, times)
                    best_machine = machine
                    processing_time = time

        # Schedule the operation on the selected machine
        job_id, op_num, machines, times = best_op
        start_time = max(machine_load[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_time[job_id] = end_time
        
        # Remove the scheduled operation from the list of operations
        operations.remove(best_op)
        
    return schedule
