
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes jobs with fewer remaining operations and 
    assigns operations to machines with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_current_op = {job: 0 for job in jobs_data}
    job_completion_time = {job: 0 for job in jobs_data}
    remaining_ops = {job: len(ops) for job, ops in jobs_data.items()}

    unassigned_operations = [(job, op_idx) for job, ops in jobs_data.items() for op_idx in range(len(ops))]

    while unassigned_operations:
        # Prioritize jobs with fewest remaining operations
        job_op_priority = sorted(unassigned_operations, key=lambda x: remaining_ops[x[0]])

        job, op_idx = job_op_priority[0]
        unassigned_operations.remove((job, op_idx))
        
        ops = jobs_data[job]
        machines, times = ops[op_idx]
        op_num = op_idx + 1
            
        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        min_end_time = float('inf')

        for i, m in enumerate(machines):
            start_time = max(machine_available_time[m], job_completion_time[job])
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                processing_time = times[i]

        if job not in schedule:
            schedule[job] = []

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time
        schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': processing_time})
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        remaining_ops[job] -= 1

    return schedule
