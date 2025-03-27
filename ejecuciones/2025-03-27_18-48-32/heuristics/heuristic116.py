
def heuristic(input_data):
    """Implements a greedy heuristic prioritizing machine utilization."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in jobs:
        schedule[job_id] = []

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, operation in enumerate(job_ops):
            operations.append((job_id, op_idx))

    # Sort operations to prioritize operations with fewer machine options first
    operations.sort(key=lambda x: len(jobs[x[0]][x[1]][0]))

    for job_id, op_idx in operations:
        operation = jobs[job_id][op_idx]
        possible_machines = operation[0]
        possible_times = operation[1]
        
        # Find the machine that becomes available the soonest among eligible machines
        best_machine = None
        earliest_available_time = float('inf')
        
        for machine in possible_machines:
            machine_index = possible_machines.index(machine)
            processing_time = possible_times[machine_index]

            # Ensure operations within the same job are executed sequentially
            current_time = max(machine_available_time[machine], job_completion_time[job_id])

            if current_time < earliest_available_time:
                earliest_available_time = current_time
                best_machine = machine

        # Schedule the operation
        machine_index = possible_machines.index(best_machine)
        processing_time = possible_times[machine_index]
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update available times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
