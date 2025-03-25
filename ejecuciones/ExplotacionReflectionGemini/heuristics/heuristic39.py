
def heuristic(input_data):
    """A heuristic to schedule jobs on machines, considering makespan, idle time, and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}  # Keep track of when each machine is available

    # Create a list of available operations, initially containing the first operation of each job
    available_operations = []
    for job_id in jobs:
        available_operations.append((job_id, 1))  # (job_id, operation_number)

    while available_operations:
        # Select the operation with the Shortest Processing Time (SPT) among available operations
        best_op = None
        min_end_time = float('inf')

        for job_id, op_num in available_operations:
            machines, times = jobs[job_id][op_num - 1]
            
            # Find the earliest available time for this operation on any suitable machine
            earliest_start_time = float('-inf')
            chosen_machine = None
            
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], (schedule[job_id][-1]['End Time'] if job_id in schedule and schedule[job_id] else 0)) if op_num > 1 else machine_available_times[m]
                end_time = start_time + times[m_idx]
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    earliest_start_time = start_time
                    best_op = (job_id, op_num, m, times[m_idx])
                    
        # Schedule the selected operation
        job_id, op_num, assigned_machine, processing_time = best_op

        start_time = max(machine_available_times[assigned_machine], (schedule[job_id][-1]['End Time'] if job_id in schedule and schedule[job_id] else 0)) if op_num > 1 else machine_available_times[assigned_machine]

        end_time = start_time + processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({'Operation': op_num, 'Assigned Machine': assigned_machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': processing_time})
        
        # Update machine availability
        machine_available_times[assigned_machine] = end_time

        # Remove the scheduled operation from available operations
        available_operations.remove((job_id, op_num))

        # Add the next operation of the job to available operations if it exists
        if op_num < len(jobs[job_id]):
            available_operations.append((job_id, op_num + 1))
    
    return schedule
