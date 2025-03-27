
def heuristic(input_data):
    """Schedules jobs using a shortest processing time and earliest available machine heuristic."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_loads = {m: 0 for m in range(n_machines)} # Track load to balance

    for job in jobs:
        schedule[job] = []

    # Flatten operations to sort them, also keeping track of the corresponding job
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time first and smallest machine id when the proccessing time is equal
    operations.sort(key=lambda x: (min(x[3]), min(x[2])))

    job_completion_times = {job: 0 for job in jobs} # Track earliest start time

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        
        # Find the machine with the earliest available time among feasible machines
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        
        for machine_index, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_times[job])
            if start_time < best_start_time:
                best_machine = machine
                best_start_time = start_time
                best_processing_time = times[machine_index]

        # Schedule the operation on the selected machine
        end_time = best_start_time + best_processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine available time and load
        machine_available_time[best_machine] = end_time
        machine_loads[best_machine] += best_processing_time
            
        #Update Job completeion time
        job_completion_times[job] = end_time

    return schedule
