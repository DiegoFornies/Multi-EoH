
def heuristic(input_data):
    """
    Schedules jobs minimizing makespan using a shortest processing time and earliest start time heuristic.
    Considers machine availability and job precedence.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    for job in jobs:
        schedule[job] = []

    # Flatten the job dictionary into a list of (job, operation_index) tuples
    operations_to_schedule = []
    for job in jobs:
        for op_idx in range(len(jobs[job])):
            operations_to_schedule.append((job, op_idx))

    # Sort the operations based on shortest processing time
    operations_to_schedule.sort(key=lambda x: min(jobs[x[0]][x[1]][1]))  # SPT

    for job, op_idx in operations_to_schedule:
        machines, times = jobs[job][op_idx]
        operation_number = op_idx + 1

        # Find the machine that allows the earliest start time.
        best_machine = None
        earliest_start = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_availability[machine], job_completion_times[job])

            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Assign the operation to the best machine and update schedules.
        start_time = earliest_start
        end_time = start_time + best_processing_time

        schedule[job].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_availability[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
