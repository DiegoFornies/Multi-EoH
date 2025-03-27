
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
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            available_machines = list(range(len(machines)))
            
            # Randomly select a machine
            machine_idx = random.choice(available_machines)
            assigned_machine = machines[machine_idx]
            processing_time = times[machine_idx]

            # Find the earliest possible start time, avoid time overlap
            start_time = max(machine_time[assigned_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_time[assigned_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
