
def heuristic(input_data):
    """
    Schedules jobs minimizing makespan by prioritizing operations with the shortest processing time
    and earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)} #Initialize all jobs completion time
    
    # Create a list of operations and their associated job, operation number, and processing times.
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on the minimum processing time across all possible machines.
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        best_machine, best_time, start_time = None, float('inf'), None
        
        #Find the best machine available
        for i, machine in enumerate(machines):
            possible_start_time = max(machine_available_time[machine], job_completion_time[job])
            if times[i] < best_time or (times[i] == best_time and possible_start_time < start_time) or best_machine is None:
                best_machine = machine
                best_time = times[i]
                start_time = possible_start_time

        end_time = start_time + best_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time  #Update completion time for the current job

    return schedule
