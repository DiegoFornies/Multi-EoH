
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules jobs based on shortest processing time and earliest machine availability.
    Prioritizes minimizing job idle time and balancing machine load.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}  # When each machine is next available
    job_completion_time = {j: 0 for j in jobs}  # When each job is next available (due to operation sequencing)
    machine_loads = {m: 0 for m in range(n_machines)} # Keep track of Machine Loads

    schedule = {}
    for job_id in jobs:
        schedule[job_id] = []

    #Create a list of operations, with job_id and op_index
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx))

    #Sort operations based on shortest processing time available
    operations.sort(key=lambda op: min(input_data['jobs'][op[0]][op[1]][1]))

    for job_id, op_idx in operations:
        machines, times = jobs[job_id][op_idx]
        possible_machines = list(zip(machines, times))
        #Sort Machines by earliest available time
        possible_machines.sort(key=lambda mt: machine_available_time[mt[0]])
        
        # Find the best machine based on earliest available time and minimum processing time given the current machine load
        best_machine = possible_machines[0][0]
        min_end_time = float('inf')

        for machine, time in possible_machines:
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + time
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_time = time

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time
        processing_time = best_time
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        machine_loads[best_machine] += processing_time
    return schedule
