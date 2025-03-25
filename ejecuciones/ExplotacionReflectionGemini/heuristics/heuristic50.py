
def heuristic(input_data):
    """Schedules operations by prioritizing jobs with fewer remaining operations and minimizing completion time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_operations = {j: len(jobs_data[j]) for j in jobs_data}
    scheduled_operations = {j: 0 for j in jobs_data}

    while any(remaining_operations.values()):
        eligible_jobs = [j for j in jobs_data if remaining_operations[j] > 0]
        if not eligible_jobs:
            break

        job = min(eligible_jobs, key=lambda j: remaining_operations[j])
        op_idx = scheduled_operations[job]
        machines, times = jobs_data[job][op_idx]

        best_machine, min_end_time, best_processing_time = -1, float('inf'), -1

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        remaining_operations[job] -= 1
        scheduled_operations[job] += 1

    return schedule
