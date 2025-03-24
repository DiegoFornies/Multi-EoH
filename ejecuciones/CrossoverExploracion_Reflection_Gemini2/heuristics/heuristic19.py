
def heuristic(input_data):
    """A scheduling heuristic that prioritizes operations based on shortest processing time (SPT) and earliest available machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of operations with their attributes
    eligible_operations = []
    for job_id, operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations):
            eligible_operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })
    
    # Sort the eligible operations based on the shortest processing time
    eligible_operations = sorted(eligible_operations, key=lambda x: min(x['times']))

    while eligible_operations:
        best_op = None
        best_machine = None
        earliest_start_time = float('inf')

        # Iterate through the remaining operations to find the best operation
        for op in eligible_operations:
            job_id = op['job_id']
            machines = op['machines']
            times = op['times']

            # Iterate through the possible machines for the current operation
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time_on_machine = machine_available_times[machine]
                
                # Ensure sequence feasibility with job completion times
                start_time = max(available_time_on_machine, job_completion_times[job_id])
                
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_op = op
                    best_machine = machine
                    best_time = processing_time

        # Assign the best operation to the best machine
        job_id = best_op['job_id']
        op_idx = best_op['op_idx']

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_time

        # Update schedule and available times
        if job_id not in schedule:
            schedule[job_id] = []

        op_num = op_idx + 1
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        
        # Remove the assigned operation from the eligible operations
        eligible_operations.remove(best_op)
        
    return schedule
