
def heuristic(input_data):
    """Schedules using shortest processing time and machine idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs.keys()}

    for job_id in jobs:
        schedule[job_id] = []
        for op_num, operation in enumerate(jobs[job_id]):
            machines, times = operation
            eligible_machines = []

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                eligible_machines.append((machine, start_time, times[i]))

            # Select machine that minimizes operation finish time
            best_machine = min(eligible_machines, key=lambda x: x[1] + x[2])
            assigned_machine, start_time, processing_time = best_machine

            end_time = start_time + processing_time
            schedule[job_id].append({
                'Operation': op_num + 1,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[assigned_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
