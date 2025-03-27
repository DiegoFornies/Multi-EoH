
def heuristic(input_data):
    """Prioritizes operations with shortest processing time, balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    for job in jobs:
        schedule[job] = []

    operation_queue = []
    for job, operations in jobs.items():
        operation_queue.append((job, 0))

    while operation_queue:
        # Sort operation_queue based on shortest processing time
        operation_queue.sort(key=lambda x: min(jobs[x[0]][x[1]][1]))

        job_id, op_index = operation_queue.pop(0)
        machines, times = jobs[job_id][op_index]

        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        # Find the machine with the earliest finish time
        for machine, time in zip(machines, times):
            start_time = max(machine_available_time[machine],
                             schedule[job_id][-1]['End Time'] if op_index > 0 else 0)
            finish_time = start_time + time

            if finish_time < best_start_time:
                best_machine = machine
                best_start_time = start_time
                best_processing_time = time

        operation = {
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        }
        schedule[job_id].append(operation)

        machine_available_time[best_machine] = best_start_time + best_processing_time

        if op_index + 1 < len(jobs[job_id]):
            operation_queue.append((job_id, op_index + 1))

    return schedule
