
def heuristic(input_data):
    """Schedules jobs using Shortest Processing Time (SPT) and earliest machine available."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    operations = []
    for job in jobs:
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            min_time = float('inf')
            for time in times:
                min_time = min(min_time, time)
            operations.append((job, op_idx, min_time))

    operations.sort(key=lambda x: x[2])  # Sort by shortest processing time

    for job, op_idx, _ in operations:
        machines, times = jobs[job][op_idx]
        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = max(machine_time[best_machine], job_completion_time[job])
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

        machine_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
