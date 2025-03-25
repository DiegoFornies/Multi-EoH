
def heuristic(input_data):
    """
    A heuristic algorithm for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes operations with shorter processing times and lower machine utilization.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    remaining_operations = {j: 0 for j in range(1, n_jobs + 1)}

    # Initialize the number of remaining operations for each job
    for job in jobs_data:
        remaining_operations[job] = len(jobs_data[job])

    # Create a list of operations that are ready to be scheduled
    ready_operations = []
    for job in jobs_data:
        if remaining_operations[job] > 0:
            ready_operations.append((job, 1))  # (job_id, operation_number)

    scheduled_operations = 0
    while scheduled_operations < sum(remaining_operations.values()):
        # Filter the list of ready operations to only include operations whose predecessors are completed
        eligible_operations = []
        for job, op_num in ready_operations:
            if op_num == 1 or schedule[job][op_num - 2]['End Time'] > 0:
                eligible_operations.append((job, op_num))
                
        if not eligible_operations:
            break
        
        # Create a dictionary of possible operation schedules
        possible_schedules = {}
        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]
            possible_schedules[(job, op_num)] = []

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_times[machine], job_completion_times[job])
                end_time = start_time + processing_time

                possible_schedules[(job, op_num)].append({
                    'Machine': machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

        # Select the operation with the minimum end time on the least utilized machine
        best_operation = None
        min_end_time = float('inf')
        least_utilized_machine = None
        
        for (job, op_num), possible_machines in possible_schedules.items():
            for schedule_option in possible_machines:
                machine = schedule_option['Machine']
                end_time = schedule_option['End Time']
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job, op_num)
                    least_utilized_machine = machine

        # Schedule the best operation on its selected machine
        job, op_num = best_operation
        machines, times = jobs_data[job][op_num - 1]
        machine_idx = possible_schedules[(job, op_num)][0]['Machine']
        processing_time = possible_schedules[(job, op_num)][0]['Processing Time']
        start_time = max(machine_available_times[least_utilized_machine], job_completion_times[job])
        end_time = start_time + processing_time
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': least_utilized_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_times[least_utilized_machine] = end_time
        job_completion_times[job] = end_time
        
        remaining_operations[job] -= 1
        scheduled_operations += 1

        # Update the list of ready operations
        ready_operations = []
        for j in jobs_data:
            next_op = len(schedule[j]) + 1
            if next_op <= len(jobs_data[j]):
                ready_operations.append((j, next_op))

    return schedule
