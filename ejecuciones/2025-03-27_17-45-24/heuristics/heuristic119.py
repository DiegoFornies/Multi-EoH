
def heuristic(input_data):
    """FJSSP heuristic: Combines EFT with load balancing and separation to minimize makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []

    operation_queue = []
    for job, operations in jobs.items():
        operation_queue.append((job, 0))

    while operation_queue:
        job_id, op_index = operation_queue.pop(0)
        machines, times = jobs[job_id][op_index]

        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        # Earliest Finish Time (EFT)
        for machine, time in zip(machines, times):
            start_time = max(machine_available_time[machine],
                             schedule[job_id][-1]['End Time'] if op_index > 0 else 0)
            finish_time = start_time + time
            
            #Consider Machine Load
            load_factor = machine_load[machine]
            # Combine EFT and load balancing
            priority = finish_time + 0.1 * load_factor

            if priority < best_start_time:
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
        machine_load[best_machine] += best_processing_time

        if op_index + 1 < len(jobs[job_id]):
            operation_queue.append((job_id, op_index + 1))

    return schedule
