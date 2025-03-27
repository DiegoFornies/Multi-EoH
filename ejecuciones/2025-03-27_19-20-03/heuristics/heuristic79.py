
def heuristic(input_data):
    """Heuristic for FJSSP: Random machine selection with lookahead."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    operation_queue = []
    for job, operations in jobs_data.items():
        operation_queue.append((job, 0))

    while operation_queue:
        job_id, op_index = operation_queue.pop(0)  # FIFO

        machines, times = jobs_data[job_id][op_index]
        
        # Randomly select a feasible machine.
        available_machines = []
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            available_machines.append((machine, processing_time, start_time))
            
        if not available_machines:
            #If no possible machine is available. skip the operation
            continue

        best_machine, best_processing_time, start_time  = random.choice(available_machines)
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        if op_index + 1 < len(jobs_data[job_id]):
            operation_queue.append((job_id, op_index + 1))

    return schedule
