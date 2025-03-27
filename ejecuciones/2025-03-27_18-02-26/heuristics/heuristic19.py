
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP)
    aiming to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []

    # Prioritize operations based on shortest processing time first (SPT)
    operation_queue = []
    for job, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            min_time = float('inf')
            best_machine = None
            for i in range(len(machines)):
                if times[i] < min_time:
                    min_time = times[i]
                    best_machine = machines[i]

            operation_queue.append((job, op_idx, best_machine, min_time))  # Include machine

    operation_queue.sort(key=lambda x: x[3])  # Sort by shortest processing time

    job_completion_time = {job: 0 for job in jobs}

    while operation_queue:
        job, op_idx, selected_machine, processing_time = operation_queue.pop(0)
        op_num = op_idx + 1

        available_time = max(machine_time[selected_machine], job_completion_time[job])

        start_time = available_time
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': selected_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_time[selected_machine] = end_time
        job_completion_time[job] = end_time
        machine_load[selected_machine] += processing_time

    return schedule
