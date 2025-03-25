
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes machine load balancing and job completion time.
    It iterates through operations, selecting the machine that minimizes the increase in machine load,
    while also considering the job's earliest possible start time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}  # When each machine is next available
    job_completion_time = {j: 0 for j in jobs}  # When each job is next available to start an operation
    machine_load = {m: 0 for m in range(n_machines)} #Total load on each machine.
    schedule = {}

    for job_id in jobs:
        schedule[job_id] = []

    # Create a list of operations to schedule
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx, op_data)) # (job_id, op_index, (machines, times))

    #Sort the operations by SPT
    operations = sorted(operations, key = lambda x: min(x[2][1]))
    
    while operations:
        best_job, best_op_idx, best_op_data = None, None, None
        best_machine, best_start_time, best_end_time, best_processing_time = None, None, None, None
        min_impact = float('inf') # Initialize impact to infinity
    
        for job_id, op_idx, op_data in operations:
            available_machines, processing_times = op_data
    
            for machine_idx, machine in enumerate(available_machines):
                processing_time = processing_times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Calculate the impact on machine load
                machine_load_impact = (machine_load[machine] + processing_time)
                
                # Combine both impacts
                impact = machine_load_impact

                if impact < min_impact:
                    min_impact = impact
                    best_job, best_op_idx, best_op_data = job_id, op_idx, op_data
                    best_machine = machine
                    best_start_time = start_time
                    best_end_time = end_time
                    best_processing_time = processing_time
    
        # Schedule the best operation
        schedule[best_job].append({
            'Operation': best_op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_end_time,
            'Processing Time': best_processing_time
        })
    
        # Update machine and job availability
        machine_available_time[best_machine] = best_end_time
        job_completion_time[best_job] = best_end_time
        machine_load[best_machine] += best_processing_time
    
        # Remove scheduled operation from the list
        operations.remove((best_job, best_op_idx, best_op_data))

    return schedule
