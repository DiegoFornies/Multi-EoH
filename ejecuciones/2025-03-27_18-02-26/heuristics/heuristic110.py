
def heuristic(input_data):
    """Prioritizes minimizing makespan and machine idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: [i for i in range(len(ops))] for job, ops in jobs.items()}

    available_operations = []
    for job in jobs:
        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))

    while available_operations:
        # Prioritize operations based on shortest processing time on any available machine
        best_op = None
        shortest_duration = float('inf')

        for job, op_idx in available_operations:
            machines, times = jobs[job][op_idx]
            for m_idx, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                duration = times[m_idx]
                if duration < shortest_duration:
                    shortest_duration = duration
                    best_op = (job, op_idx, m, duration, start_time)

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
        machine_time[assigned_machine] = end_time
        job_completion_time[job] = end_time

        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))

        available_operations.remove((job, op_idx))

    return schedule
