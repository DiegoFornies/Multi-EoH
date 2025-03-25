
def heuristic(input_data):
    """Combines machine load and SPT for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    solution = {}
    for job_id in jobs:
        solution[job_id] = []

    available_operations = []
    for job_id in jobs:
        available_operations.append((job_id, 1))

    while available_operations:
        best_op = None
        min_end_time = float('inf')

        for job_id, op_num in available_operations:
            machines, times = jobs[job_id][op_num - 1]
            earliest_start_time = float('inf')
            chosen_machine = None
            best_processing_time = None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_start_time:
                    earliest_start_time = end_time
                    chosen_machine = machine
                    best_processing_time = processing_time

            if chosen_machine is not None and earliest_start_time < min_end_time:
                min_end_time = earliest_start_time
                best_op = (job_id, op_num, chosen_machine, best_processing_time, earliest_start_time)

        if best_op is None:
            break

        job_id, op_num, assigned_machine, processing_time, start_time = best_op

        end_time = start_time + processing_time

        if job_id not in solution:
            solution[job_id] = []

        solution[job_id].append({
            'Operation': op_num,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        machine_available_times[assigned_machine] = end_time
        job_completion_times[job_id] = end_time
        available_operations.remove((job_id, op_num))

        if op_num < len(jobs[job_id]):
            available_operations.append((job_id, op_num + 1))

    return solution
