
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_loads = {m: 0 for m in range(n_machines)}

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_index in range(len(jobs_data[job_id])):
            operations.append((job_id, op_index))

    operations.sort(key=lambda x: len(jobs_data[x[0]][x[1]][0]))

    for job_id, op_index in operations:
        machines, times = jobs_data[job_id][op_index]
        
        best_machine = None
        min_finish_time = float('inf')
        
        for m_index, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            finish_time = start_time + times[m_index]

            if finish_time < min_finish_time:
                min_finish_time = finish_time
                best_machine = machine
                processing_time = times[m_index]
                start_time_selected = start_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time_selected,
            'End Time': start_time_selected + processing_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = start_time_selected + processing_time
        job_completion_time[job_id] = start_time_selected + processing_time
        machine_loads[best_machine] += processing_time

    return schedule
