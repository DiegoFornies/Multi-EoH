
def heuristic(input_data):
    """Prioritize operations with shortest processing time on least loaded machines."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    operation_queue = []

    for job in jobs:
        if job not in schedule:
            schedule[job] = []

        for op_idx, (machines, times) in enumerate(jobs[job]):
            min_time = min(times)
            operation_queue.append((min_time, job, op_idx))

    operation_queue.sort()

    while operation_queue:
        min_time, job, op_idx = operation_queue.pop(0)
        machines, times = jobs[job][op_idx]

        best_machine = None
        min_makespan = float('inf')
        best_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            makespan = max(machine_load[machine], (schedule[job][-1]['End Time'] if op_idx > 0 else 0)) + processing_time
            if makespan < min_makespan:
                min_makespan = makespan
                best_machine = machine
                best_time = processing_time

        start_time = max(machine_load[best_machine], (schedule[job][-1]['End Time'] if op_idx > 0 else 0))
        end_time = start_time + best_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_load[best_machine] = end_time

    return schedule
