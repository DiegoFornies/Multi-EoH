
def heuristic(input_data):
    """Prioritizes operations with shortest processing time, considering machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the machine that allows the operation to start earliest
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_time[machine], job_completion_time[job_id])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = times[i]

        # Schedule the operation on the best machine
        start_time = earliest_start_time
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job states
        machine_time[best_machine] = end_time
        machine_load[best_machine] += best_processing_time
        job_completion_time[job_id] = end_time

    return schedule
