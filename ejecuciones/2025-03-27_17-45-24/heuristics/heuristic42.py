
def heuristic(input_data):
    """Combines EFT and shortest remaining time for balanced FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    remaining_times = {}

    for job in jobs:
        schedule[job] = []
        remaining_times[job] = sum(times[0] for _, times in jobs[job])

    operation_queue = []
    for job, operations in jobs.items():
        operation_queue.append((job, 0))

    while operation_queue:
        # Prioritize jobs with shortest remaining time
        job_id, op_index = min(operation_queue, key=lambda x: remaining_times[x[0]])
        operation_queue.remove((job_id, op_index))

        machines, times = jobs[job_id][op_index]

        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        # Earliest Finish Time
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
        remaining_times[job_id] -= best_processing_time

        if op_index + 1 < len(jobs[job_id]):
            operation_queue.append((job_id, op_index + 1))

    return schedule
