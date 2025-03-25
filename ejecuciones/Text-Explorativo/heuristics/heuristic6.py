
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with shorter processing times
    and assigns them to the least loaded machine to balance the load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    eligible_operations = []  # (job, op_idx, machines, times)
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 0, operations[0][0], operations[0][1]))

    scheduled_operations = set()
    while eligible_operations:
        # Prioritize operations with shortest processing time
        eligible_operations.sort(key=lambda x: min(x[3]))

        job, op_idx, machines, times = eligible_operations.pop(0)
        
        # Find the least loaded machine among feasible machines
        best_machine = machines[0]
        min_load = float('inf')

        for i, machine in enumerate(machines):
            if machine_load[machine] < min_load:
                min_load = machine_load[machine]
                best_machine = machine

        processing_time = times[machines.index(best_machine)] # select right processing time

        # Schedule the operation on the chosen machine
        start_time = max(machine_load[best_machine], job_completion_times[job])
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[job] = end_time

        scheduled_operations.add((job, op_idx))

        # Add the next operation of the job to eligible operations if it exists
        next_op_idx = op_idx + 1
        if next_op_idx < len(jobs_data[job]):
            eligible_operations.append((job, next_op_idx, jobs_data[job][next_op_idx][0], jobs_data[job][next_op_idx][1]))
            
    return schedule
