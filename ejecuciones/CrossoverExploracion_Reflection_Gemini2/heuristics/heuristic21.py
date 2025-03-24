
def heuristic(input_data):
    """
    A heuristic for FJSSP aiming to minimize makespan and balance machine load.
    Prioritizes operations with shorter processing times and machines with earlier availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by shortest processing time first
    operations.sort(key=lambda x: min(x[3]))  # x[3] is times list

    for job, op_num, machines, times in operations:
        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + times[i]  #times[i] corresponds to the processing time on that machine

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = times[i] # Save the process time corresponding with the chosen machine
        
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
