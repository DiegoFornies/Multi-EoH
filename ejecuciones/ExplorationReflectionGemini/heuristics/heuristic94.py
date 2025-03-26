
def heuristic(input_data):
    """Schedules jobs using a priority rule based on operation slack."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Calculate total work remaining for each job
    job_remaining_work = {}
    for job_id in range(1, n_jobs + 1):
        remaining_work = 0
        for operation_data in jobs[job_id]:
            remaining_work += min(operation_data[1])  # Shortest processing time
        job_remaining_work[job_id] = remaining_work

    # Operation Prioritization (Slack First)
    operation_queue = []
    for job_id in range(1, n_jobs + 1):
        job_operations = jobs[job_id]
        for operation_index, operation_data in enumerate(job_operations):
            operation_queue.append((job_id, operation_index))

    # Schedule Operations based on slack
    scheduled_operations = set()
    while operation_queue:
        best_op = None
        min_slack = float('inf')

        # Find the operation with the minimum slack
        for job_id, operation_index in operation_queue:
            available_machines = jobs[job_id][operation_index][0]
            available_times = jobs[job_id][operation_index][1]
            
            # Calculate earliest possible start time
            min_start_time = float('inf')
            for machine_index, machine in enumerate(available_machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                min_start_time = min(min_start_time, start_time)
            
            # Slack is the difference between remaining work and earliest start time
            slack = min_start_time + job_remaining_work[job_id] - min(available_times)

            if slack < min_slack:
                min_slack = slack
                best_op = (job_id, operation_index)
        
        if best_op is None:
          break
          
        job_id, operation_index = best_op
        operation_data = jobs[job_id][operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        # Select machine based on earliest availability
        best_machine = None
        earliest_end_time = float('inf')

        for i in range(len(possible_machines)):
            machine = possible_machines[i]
            processing_time = possible_times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            end_time = start_time + processing_time
            if end_time < earliest_end_time:
                earliest_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Update schedules and times
        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time
        job_remaining_work[job_id] -= best_processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        operation_queue.remove((job_id, operation_index))

    return schedule
