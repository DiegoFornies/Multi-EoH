
def heuristic(input_data):
    """Heuristic for FJSSP: Combines earliest start time and SPT."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    remaining_operations = {j: len(jobs[j]) for j in jobs}
    scheduled_operations = {j: 0 for j in jobs}

    while any(remaining_operations.values()):
        eligible_jobs = [j for j in jobs if remaining_operations[j] > 0]
        if not eligible_jobs:
            break

        # Prioritize jobs with fewer remaining operations (SPT)
        job = min(eligible_jobs, key=lambda j: remaining_operations[j])

        op_idx = scheduled_operations[job]
        machines, times = jobs[job][op_idx]

        # Find the machine with the earliest available time
        best_machine, best_time = None, float('inf')
        earliest_start = float('inf')

        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = processing_time

        start_time = earliest_start
        end_time = start_time + best_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        remaining_operations[job] -= 1
        scheduled_operations[job] += 1

    return schedule
