
def heuristic(input_data):
    """Operation-centric heuristic with makespan and balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    machine_times = {m: 0 for m in range(n_machines)}
    machine_loads = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    operations = []
    for job_id in jobs:
        for op_index, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_index, op_data))

    operations.sort(key=lambda x: x[0])

    for job_id, op_index, op_data in operations:
        machines, times = op_data
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_times[machine], job_completion[job_id])
            end_time = start_time + times[i]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[i]

        start_time = max(machine_times[best_machine], job_completion[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_times[best_machine] = end_time
        machine_loads[best_machine] += processing_time
        job_completion[job_id] = end_time

    return schedule
