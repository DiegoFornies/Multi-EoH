
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations based on shortest processing time.
    It attempts to balance machine load by selecting the least loaded machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    remaining_operations = {}
    for job, operations in jobs_data.items():
        remaining_operations[job] = [(i + 1, op) for i, op in enumerate(operations)]

    scheduled_operations = []

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, ops in remaining_operations.items():
            if ops:
                op_num, (machines, times) = ops[0]
                eligible_operations.append((job, op_num, machines, times))
        
        if not eligible_operations:
            break # Handle empty list to avoid errors

        # Prioritize operations with shortest possible processing time
        eligible_operations.sort(key=lambda x: min(x[3]))

        # Select the operation
        job_to_schedule, op_num_to_schedule, machines_to_schedule, times_to_schedule = eligible_operations[0]

        # Choose machine with least load for the selected operation
        available_machines = [(m, t) for m, t in zip(machines_to_schedule, times_to_schedule)]
        best_machine = min(available_machines, key=lambda x: machine_load[x[0]])[0]
        processing_time = available_machines[0][1] if best_machine == available_machines[0][0] else available_machines[1][1] if len(available_machines) > 1 and best_machine == available_machines[1][0] else available_machines[0][1]

        # Determine start time based on machine availability and job completion time
        start_time = max(machine_load[best_machine], job_completion_times[job_to_schedule])
        end_time = start_time + processing_time
        
        # Update schedule
        if job_to_schedule not in schedule:
            schedule[job_to_schedule] = []
        schedule[job_to_schedule].append({
            'Operation': op_num_to_schedule,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[job_to_schedule] = end_time

        # Remove the scheduled operation from remaining operations
        remaining_operations[job_to_schedule].pop(0)
        scheduled_operations.append((job_to_schedule, op_num_to_schedule))

    return schedule
