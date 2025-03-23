
def heuristic(input_data):
    """
    FJSSP heuristic: Prioritizes operations based on earliest start time,
    minimizing makespan and respecting job/machine constraints.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    available_operations = {job_id: 0 for job_id in jobs_data.keys()}
    operations_to_schedule = []
    for job_id, job_data in jobs_data.items():
        operations_to_schedule.append((job_id, 0))

    while operations_to_schedule:
        operations_to_schedule.sort(key=lambda x: max(job_completion_time[x[0]], min([machine_available_time[m] for m in jobs_data[x[0]][x[1]][0]])))
        job_id, operation_index = operations_to_schedule.pop(0)
        machines, times = jobs_data[job_id][operation_index]

        best_machine = None
        min_completion_time = float('inf')
        best_processing_time = 0

        for machine_idx, machine in enumerate(machines):
            start_time = max(job_completion_time[job_id], machine_available_time[machine])
            completion_time = start_time + times[machine_idx]
            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_processing_time = times[machine_idx]

        start_time = max(job_completion_time[job_id], machine_available_time[best_machine])
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        if operation_index + 1 < len(jobs_data[job_id]):
            operations_to_schedule.append((job_id, operation_index + 1))

    return schedule
