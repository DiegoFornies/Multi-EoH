
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that prioritizes
    operations with shorter processing times and balances machine load.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}  # Earliest time machine m is available.
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}   # Completion time of the last scheduled operation of job j.

    # Operations that are ready to be scheduled. Initially, the first operation of each job is ready.
    ready_operations = {job: 0 for job in jobs}  # Index of the next operation to schedule for each job.

    # All operations represented as a list of tuples (job_id, operation_index).
    all_operations = []
    for job_id in jobs:
        for operation_index in range(len(jobs[job_id])):
            all_operations.append((job_id, operation_index))

    # Sort operations by shortest processing time (SPT) of their first available machine.
    def sort_key(operation):
        job_id, operation_index = operation
        machines, times = jobs[job_id][operation_index]
        return min(times)

    scheduled_count = 0
    while scheduled_count < len(all_operations):
        # Collect candidate operations.
        candidate_operations = []
        for job_id in jobs:
            op_idx = ready_operations[job_id]
            if op_idx < len(jobs[job_id]):
                candidate_operations.append((job_id, op_idx))
        
        if not candidate_operations:
          break # no more operations to schedule
        
        # Select the operation with the shortest processing time among the candidates.
        best_operation = min(candidate_operations, key=sort_key)
        job_id, operation_index = best_operation
        machines, times = jobs[job_id][operation_index]

        # Choose the machine with the earliest available time among the feasible machines.
        best_machine = min(range(len(machines)), key=lambda i: max(machine_available_times[machines[i]], job_completion_times[job_id]))
        assigned_machine = machines[best_machine]
        processing_time = times[best_machine]

        # Determine the start and end times for the operation.
        start_time = max(machine_available_times[assigned_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        # Update the schedule.
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time.
        machine_available_times[assigned_machine] = end_time
        job_completion_times[job_id] = end_time

        # Mark the next operation in the job as ready.
        ready_operations[job_id] += 1
        scheduled_count +=1
    return schedule
