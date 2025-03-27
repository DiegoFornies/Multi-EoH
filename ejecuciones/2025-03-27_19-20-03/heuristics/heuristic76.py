
def heuristic(input_data):
    """Heuristic for FJSSP: Random machine assignment with makespan minimization."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            
            # Randomly select a machine from the available machines
            selected_machine_index = random.randint(0, len(machines) - 1)
            selected_machine = machines[selected_machine_index]
            processing_time = times[selected_machine_index]

            # Determine the start time based on machine and job availability
            start_time = max(machine_time[selected_machine], job_completion_time[job])
            end_time = start_time + processing_time

            # Update the schedule
            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': selected_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_time[selected_machine] = end_time
            job_completion_time[job] = end_time
            current_time = end_time

    return schedule
