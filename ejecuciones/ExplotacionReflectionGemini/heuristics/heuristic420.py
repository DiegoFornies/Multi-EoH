
def heuristic(input_data):
    """FJSSP heuristic: Minimize makespan then balance load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()

    while available_operations:
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        job_id, op_idx = best_operation
        machine, processing_time = best_machine

        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))
    # Balance Machine Load - Post Processing
    machine_loads = {m: 0 for m in range(n_machines)}
    for job_id in schedule:
        for operation in schedule[job_id]:
            machine_loads[operation['Assigned Machine']] += operation['Processing Time']

    max_load_machine = max(machine_loads, key=machine_loads.get)
    min_load_machine = min(machine_loads, key=machine_loads.get)

    # Find an operation on max_load_machine that can be moved to min_load_machine
    for job_id in schedule:
        for op_idx, operation in enumerate(schedule[job_id]):
            if operation['Assigned Machine'] == max_load_machine:
                job_def = input_data['jobs'][job_id][operation['Operation']-1]
                possible_machines = job_def[0]
                possible_times = job_def[1]

                if min_load_machine in possible_machines and min_load_machine != max_load_machine:

                    new_processing_time = possible_times[possible_machines.index(min_load_machine)]
                    # Calculate new start and end times
                    old_machine = operation['Assigned Machine']
                    old_start_time = operation['Start Time']

                    # Update operation
                    operation['Assigned Machine'] = min_load_machine
                    operation['Processing Time'] = new_processing_time

                    # Adjust Start time based on machine availability
                    operation['Start Time'] = max(machine_available_time[min_load_machine], job_completion_time[job_id] - operation['Processing Time'])
                    operation['End Time'] = operation['Start Time'] + operation['Processing Time']

                    #update job completion time
                    job_completion_time[job_id] = max(job_completion_time[job_id], operation['End Time'])

                    # Update Machine Availability
                    machine_available_time[min_load_machine] = operation['End Time']
                    machine_loads[old_machine] -= (old_start_time + operation['Processing Time']) #This is to simply reduce the overall load
                    machine_loads[min_load_machine] += operation['Processing Time'] #Adjusts total load on new machine

                    return schedule #Just moving one for now since makespan reduction is more important

    return schedule
