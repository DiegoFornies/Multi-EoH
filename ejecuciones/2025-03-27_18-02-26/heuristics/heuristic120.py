
def heuristic(input_data):
    """Heuristic for FJSSP: Prioritizes minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: [i for i in range(len(ops))] for job, ops in jobs.items()}
    available_operations = []
    for job in jobs:
        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))

    while available_operations:
        # Select operation based on shortest processing time first (SPT)
        best_op = None
        shortest_time = float('inf')

        for job, op_idx in available_operations:
            machines, times = jobs[job][op_idx]

            best_machine = None
            min_start_time = float('inf')
            best_processing_time = float('inf')
            
            #find the machine that provides the earliest possible start time for this operation and prioritize shortest processing time
            for m_idx, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = m
                    best_processing_time = times[m_idx]
                elif start_time == min_start_time and times[m_idx] < best_processing_time:
                    best_machine = m
                    best_processing_time = times[m_idx]

            if best_processing_time < shortest_time:
                shortest_time = best_processing_time
                best_op = (job, op_idx, best_machine, best_processing_time, min_start_time)

        job, op_idx, assigned_machine, processing_time, start_time = best_op
        end_time = start_time + processing_time

        # Update schedule
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

        machine_time[assigned_machine] = end_time
        machine_load[assigned_machine] += processing_time
        job_completion_time[job] = end_time

        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))

        available_operations.remove((job, op_idx))

    return schedule
