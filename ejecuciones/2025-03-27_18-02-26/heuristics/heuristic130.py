
def heuristic(input_data):
    """Heuristic minimizing makespan by considering machine availability and job priority."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: [i for i in range(len(ops))] for job, ops in jobs.items()}

    def calculate_priority(job, op_idx):
        """Calculate priority based on processing time and job due date."""
        machines, times = jobs[job][op_idx]
        # Prioritize operations with shorter processing times
        min_time = min(times)
        # Early jobs have higher priority
        return min_time

    available_operations = []
    for job in jobs:
        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))

    while available_operations:
        # Select operation with the highest priority
        best_op = None
        best_priority = float('inf')  # Lower is better

        for job, op_idx in available_operations:
            priority = calculate_priority(job, op_idx)
            if priority < best_priority:
                best_priority = priority
                best_op = (job, op_idx)

        job, op_idx = best_op
        machines, times = jobs[job][op_idx]

        # Find the machine that allows the earliest start time
        best_machine = None
        best_time = None
        min_start_time = float('inf')

        for m_idx, m in enumerate(machines):
            start_time = max(machine_time[m], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                best_time = times[m_idx]

        end_time = min_start_time + best_time

        # Update schedule
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': min_start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        remaining_operations[job].pop(0)

        machine_time[best_machine] = end_time
        job_completion_time[job] = end_time

        # Add next operation if available
        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))

        available_operations.remove((job, op_idx))

    return schedule
