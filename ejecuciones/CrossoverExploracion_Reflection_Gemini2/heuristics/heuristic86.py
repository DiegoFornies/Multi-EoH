
def heuristic(input_data):
    """Hybrid heuristic: SPT for job order, least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs.keys()}
    machine_load = {m: 0 for m in range(n_machines)}

    # SPT for job order
    job_priority = sorted(jobs.keys(), key=lambda job_id: sum(min(times) for _, times in jobs[job_id]))

    for job_id in job_priority:
        schedule[job_id] = []
        for op_num, operation in enumerate(jobs[job_id]):
            machines, times = operation
            eligible_machines = []

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                eligible_machines.append((machine, start_time, times[i]))

            # Least loaded machine for this op
            best_machine = min(eligible_machines, key=lambda x: machine_load[x[0]] + x[2])
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
            machine_load[assigned_machine] += processing_time

    return schedule
