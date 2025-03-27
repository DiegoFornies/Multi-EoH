
def heuristic(input_data):
    """Combines shortest job & least loaded machine for scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    job_processing_times = {}

    for job, operations in jobs.items():
        total_time = 0
        for op in operations:
            total_time += min(op[1])
        job_processing_times[job] = total_time
    
    remaining_operations = {job: [i for i in range(len(ops))] for job, ops in jobs.items()}
    available_operations = []
    for job in jobs:
        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))

    while available_operations:
        best_op = None
        best_priority = float('inf')

        for job, op_idx in available_operations:
            machines, times = jobs[job][op_idx]
            
            best_machine = None
            min_start_time = float('inf')
            best_time = None

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = m
                    best_time = times[m_idx]

            priority = job_processing_times[job] + min_start_time

            if priority < best_priority:
                best_priority = priority
                best_op = (job, op_idx, best_machine, best_time, min_start_time)

        job, op_idx, assigned_machine, processing_time, start_time = best_op
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        remaining_operations[job].pop(0)
        
        machine_available_times[assigned_machine] = end_time
        job_completion_times[job] = end_time

        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))
            
        available_operations = [(j, o) for j, o in available_operations if (j,o) != (job, op_idx)]

    return schedule
