
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes operations with shorter processing times."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of all operations with their job and operation indices.
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx, op_data))

    # Sort the operations based on the shortest processing time first.
    operations.sort(key=lambda x: min(x[2][1]))

    for job_id, op_idx, op_data in operations:
        machines, times = op_data
        best_machine, min_completion_time = None, float('inf')

        for m_idx, machine in enumerate(machines):
            completion_time = max(machine_available_time[machine], job_completion_time[job_id]) + times[m_idx]
            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_time = times[m_idx]
        
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time
        
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
