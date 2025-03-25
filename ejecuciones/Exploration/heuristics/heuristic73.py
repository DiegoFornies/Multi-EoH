
def heuristic(input_data):
    """Schedules jobs using a priority rule based on operation slack."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    
    remaining_times = {}
    for job in jobs:
        remaining_times[job] = sum(min(t) for _, t in jobs[job])

    for job in jobs:
        schedule[job] = []

    unscheduled_operations = []
    for job in jobs:
        for op_idx, operation in enumerate(jobs[job]):
            unscheduled_operations.append((job, op_idx))

    while unscheduled_operations:
        # Calculate slack for each operation. Slack = latest possible start time - earliest possible start time
        operation_slack = {}
        
        for job, op_idx in unscheduled_operations:
            machines, times = jobs[job][op_idx]
            
            #Earliest Possible start time
            earliest_start_time = float('inf')
            best_machine = None
            processing_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    processing_time = times[m_idx]
            
            # Latest Possible start time (Critical path approach)
            
            latest_start_time = float('inf') #Initialize to a very large value
            
            dummy_completion_time = {}
            for m in range(n_machines):
                dummy_completion_time[m] = machine_available_time[m]
            
            dummy_job_completion_time = {}
            for j in jobs:
                dummy_job_completion_time[j] = job_completion_time[j]
            
            
            
            latest_start_time = float('inf')
            
            for m_idx, machine in enumerate(machines):
                
                start_time = max(dummy_completion_time[machine], dummy_job_completion_time[job])
                
                
                dummy_completion_time[machine] = start_time + times[m_idx]
                dummy_job_completion_time[job] = start_time + times[m_idx]
            
                if dummy_job_completion_time[job] < latest_start_time:
                        latest_start_time = start_time
            
            operation_slack[(job, op_idx)] = latest_start_time - earliest_start_time

        # Select operation with the minimum slack
        
        if not operation_slack:
            break

        selected_operation = min(operation_slack, key=operation_slack.get)
        job, op_idx = selected_operation
        machines, times = jobs[job][op_idx]
        op_num = op_idx + 1

        # Assign the operation to the machine that results in the earliest completion time
        best_machine = None
        min_end_time = float('inf')
        processing_time = None
        earliest_start_time = float('inf')

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + times[m_idx]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[m_idx]
                earliest_start_time = start_time

        # Update schedule
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': earliest_start_time,
            'End Time': min_end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = min_end_time
        job_completion_time[job] = min_end_time

        # Remove the scheduled operation from the unscheduled operations list
        unscheduled_operations.remove((job, op_idx))

    return schedule
