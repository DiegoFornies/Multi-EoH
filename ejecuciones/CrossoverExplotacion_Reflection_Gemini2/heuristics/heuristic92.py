
def heuristic(input_data):
    """Combines earliest start time and shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    ready_operations = []
    for job_id, operations in jobs.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        earliest_start_time = float('inf')
        best_machine = None
        best_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs[job_id][op_index]

            min_start_time = float('inf')
            selected_machine = None
            selected_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < min_start_time or (start_time == min_start_time and time < selected_time):
                    min_start_time = start_time
                    selected_machine = machine
                    selected_time = time

            if min_start_time < earliest_start_time:
                earliest_start_time = min_start_time
                best_job = job_id
                best_op_index = op_index
                best_machine = selected_machine
                best_time = selected_time
        
        job_id, op_index = best_job, best_op_index
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time
        
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        
        ready_operations.remove((job_id, op_index))
        
        if op_index + 1 < len(jobs[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
