
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shortest processing time and early machine availability
    to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        end_time = best_start_time + best_processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
