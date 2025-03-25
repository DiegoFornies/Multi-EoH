
def heuristic(input_data):
    """
    Schedules jobs by prioritizing operations with shortest processing time
    and earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    remaining_operations = {j: list(range(1, len(jobs[j]) + 1)) for j in jobs}

    scheduled_operations = []
    
    while any(remaining_operations.values()):
        eligible_operations = []
        for job in jobs:
            if remaining_operations[job]:
                op_num = remaining_operations[job][0]
                op_idx = op_num - 1
                machines, times = jobs[job][op_idx]
                eligible_operations.append((job, op_num, machines, times))

        if not eligible_operations:
            break

        best_operation = None
        min_end_time = float('inf')

        for job, op_num, machines, times in eligible_operations:
            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job, op_num, machine, processing_time, start_time, end_time)
                    
        job, op_num, assigned_machine, processing_time, start_time, end_time = best_operation

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[assigned_machine] = end_time
        job_completion_time[job] = end_time
        remaining_operations[job].pop(0)

    return schedule
