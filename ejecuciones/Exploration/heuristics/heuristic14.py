
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes operations with shorter processing times on faster machines
    to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of operations, sorted by shortest processing time
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op_data))

    operations.sort(key=lambda op: min(op[2][1]))  # Sort by minimum processing time

    for job_id, op_num, op_data in operations:
        machines, times = op_data
        best_machine, best_time = None, float('inf')

        # Find the fastest available machine for the current operation
        for i, machine in enumerate(machines):
            available_time = max(machine_available_time[machine], job_completion_time[job_id])
            if available_time + times[i] < best_time:
                best_time = available_time + times[i]
                best_machine = machine
                processing_time = times[i]

        # Schedule the operation on the selected machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
