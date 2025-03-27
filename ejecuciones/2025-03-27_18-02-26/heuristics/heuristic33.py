
def heuristic(input_data):
    """
    Prioritizes shortest processing time (SPT) among available machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation

            # Find machine with shortest processing time
            best_machine = None
            min_processing_time = float('inf')
            selected_time = None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine
                    selected_time = processing_time

            # Schedule operation
            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + selected_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': selected_time
            })

            # Update machine and job times
            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
