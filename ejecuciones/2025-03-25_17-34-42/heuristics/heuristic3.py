
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules operations based on shortest processing time and machine availability.
    Prioritizes machines with minimal load, aiming for balanced schedules and reduced makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []

    # Prioritize operations based on shortest processing time
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx, machines, times))

    operations.sort(key=lambda x: min(x[3]))  # Sort by shortest processing time

    for job_id, op_idx, machines, times in operations:
        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        min_available_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            available_time = max(machine_available_time[machine], job_completion_time[job_id])
            if available_time < min_available_time:
                min_available_time = available_time
                best_machine = machine
                best_processing_time = times[i]

        # Schedule the operation on the selected machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
