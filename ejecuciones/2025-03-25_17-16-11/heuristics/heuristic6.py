
def heuristic(input_data):
    """Aims to minimize makespan by prioritizing jobs with fewer remaining operations and shorter processing times, balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_ops = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}


    unassigned_operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs[job_id]):
            unassigned_operations.append((job_id, op_idx))

    while unassigned_operations:
        # Prioritize operations based on remaining ops in their job and processing time
        best_op = None
        min_priority = float('inf')

        for job_id, op_idx in unassigned_operations:
            machines, times = jobs[job_id][op_idx]
            #Prioritze by jobs with few remaining ops, then by shorter processing times
            priority = job_remaining_ops[job_id] + (min(times) / 1000.0)
            if priority < min_priority:
                min_priority = priority
                best_op = (job_id, op_idx)

        job_id, op_idx = best_op
        machines, times = jobs[job_id][op_idx]

        # Find the best machine for this operation (earliest available time)
        best_machine = None
        min_end_time = float('inf')

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[m_idx]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[m_idx]

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        job_remaining_ops[job_id] -= 1

        unassigned_operations.remove((job_id, op_idx))

    return schedule
