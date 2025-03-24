
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with shorter processing times.
    It aims to minimize makespan by scheduling shorter tasks first.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize data structures
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of operations with their potential start times and processing times
    eligible_operations = []
    for job_id, operations in jobs_data.items():
        eligible_operations.append((job_id, 0))  # (job_id, operation_index)

    scheduled_operations = set()

    while eligible_operations:
        # Find the operation with the shortest processing time among eligible operations
        best_operation = None
        min_duration = float('inf')

        for job_id, op_index in eligible_operations:
            machines, durations = jobs_data[job_id][op_index]
            
            # Find the machine and duration that results in the earliest possible end time for this operation
            best_machine = None
            best_duration = None
            earliest_end_time = float('inf')

            for machine_id, duration in zip(machines, durations):
                start_time = max(machine_available_time[machine_id], job_completion_time[job_id])
                end_time = start_time + duration

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_machine = machine_id
                    best_duration = duration

            if earliest_end_time < min_duration:
                min_duration = earliest_end_time
                best_operation = (job_id, op_index, best_machine, best_duration, max(machine_available_time[best_machine], job_completion_time[job_id]))

        # Schedule the best operation
        job_id, op_index, machine_id, duration, start_time = best_operation
        end_time = start_time + duration

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': machine_id,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': duration
        })

        machine_available_time[machine_id] = end_time
        job_completion_time[job_id] = end_time

        scheduled_operations.add((job_id, op_index))

        # Add the next operation of the job to the eligible operations
        if op_index + 1 < len(jobs_data[job_id]):
            eligible_operations.append((job_id, op_index + 1))

        eligible_operations.remove((job_id, op_index))
        
    return schedule
