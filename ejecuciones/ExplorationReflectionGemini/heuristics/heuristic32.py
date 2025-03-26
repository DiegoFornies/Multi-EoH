
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with shortest processing time
    among available machines, minimizing makespan and balancing machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    unassigned_operations = []

    # Create initial unassigned operations list
    for job_id, operations in jobs_data.items():
        for op_idx, op_data in enumerate(operations):
            unassigned_operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': op_data[0],
                'times': op_data[1]
            })

    # Iterate until all operations are assigned
    while unassigned_operations:
        # Find the operation with the shortest processing time
        best_operation = None
        shortest_time = float('inf')

        for op in unassigned_operations:
            job_id = op['job']
            machines = op['machines']
            times = op['times']
            op_idx = op['operation'] -1

            available_machines_times = {}
            for i, machine in enumerate(machines):
                available_machines_times[machine] = max(machine_available_time[machine], job_completion_time[job_id])

            for i, machine in enumerate(machines):
                time = times[i]
                if available_machines_times[machine] + time < shortest_time:
                     shortest_time = available_machines_times[machine] + time
                     best_operation = op
                     best_machine = machine
                     best_time = time

        # Assign the best operation to the selected machine
        job_id = best_operation['job']
        op_num = best_operation['operation']
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        # Remove the assigned operation from the unassigned list
        unassigned_operations.remove(best_operation)

    return schedule
