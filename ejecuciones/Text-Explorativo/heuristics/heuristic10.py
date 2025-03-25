
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules operations based on shortest processing time and earliest machine availability.
    Prioritizes operations with shorter processing times and assigns them to the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Prioritize operations based on shortest processing time
    operation_queue = []
    for job_id, operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations):
            operation_queue.append((job_id, op_idx, machines, times))

    # Sort operations by shortest processing time across available machines
    operation_queue.sort(key=lambda x: min(x[3]))

    for job_id, op_idx, machines, times in operation_queue:
        # Find the machine with earliest available time among feasible machines
        best_machine, best_time = None, float('inf')
        for i, machine in enumerate(machines):
            available_time = max(machine_available_time[machine], job_completion_time[job_id])
            if available_time < best_time:
                best_time = available_time
                best_machine = machine
                best_processing_time = times[i]

        start_time = best_time
        end_time = start_time + best_processing_time

        # Update schedule and machine/job completion times
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
