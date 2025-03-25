
def heuristic(input_data):
    """Combines job prioritization with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs.items()}

    job_priority = sorted(jobs.keys(), key=lambda job: len(remaining_operations[job]), reverse=True)

    while any(remaining_operations[job] for job in jobs):
        for job in job_priority:
            if not remaining_operations[job]:
                continue

            operation_number = remaining_operations[job][0]
            operation_index = operation_number - 1
            machines, times = jobs[job][operation_index]

            best_machine, best_start_time, best_end_time, best_processing_time = None, float('inf'), float('inf'), None
            min_impact = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                machine_load_impact = machine_load[machine] + processing_time
                impact = machine_load_impact

                if impact < min_impact:
                    min_impact = impact
                    best_machine, best_start_time, best_end_time, best_processing_time = machine, start_time, end_time, processing_time

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_end_time
            job_completion_time[job] = best_end_time
            machine_load[best_machine] += best_processing_time
            remaining_operations[job].pop(0)

    return schedule
