
def heuristic(input_data):
    """
    A scheduling heuristic for FJSSP that considers machine load and operation duration.
    It prioritizes machines with lower loads and operations with shorter durations.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations with their job and operation numbers
    operations = []
    for job in jobs:
        for op_idx, op_data in enumerate(jobs[job]):
            operations.append((job, op_idx + 1, op_data))

    # Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[2][1]))

    for job, op_num, op_data in operations:
        machines, times = op_data

        # Find the machine that can start the operation earliest
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = times[i]

        # Schedule the operation on the best machine
        start_time = earliest_start_time
        end_time = start_time + best_processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
