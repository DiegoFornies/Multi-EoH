
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes machine availability and job order."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_end_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            best_machine, best_time = None, float('inf')
            earliest_start = float('inf')

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_end_time[job_id])
                if start_time < earliest_start:
                  earliest_start = start_time
                  best_machine = machine
                  best_time = times[i]

            start_time = max(machine_available_time[best_machine], job_end_time[job_id])
            end_time = start_time + best_time
            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })
            machine_available_time[best_machine] = end_time
            job_end_time[job_id] = end_time

    return schedule
