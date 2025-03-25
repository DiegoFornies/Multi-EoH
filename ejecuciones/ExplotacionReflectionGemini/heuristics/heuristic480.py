
def heuristic(input_data):
    """Heuristic for FJSSP: Adaptive weights, remaining ops & separation."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_last_machine = {j: None for j in range(1, n_jobs + 1)}


    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()

    while available_operations:
        best_operation = None
        best_machine = None
        best_start_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]
            remaining_ops = len(jobs[job_id]) - op_idx - 1
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                # Adaptive weights
                idle_time_weight = 0.5
                remaining_ops_weight = 0.3
                load_weight = 0.2

                idle_time_score = start_time - machine_available_time[machine] if start_time > machine_available_time[machine] else 0
                remaining_ops_score = remaining_ops
                load_score = machine_available_time[machine]  # Prefer less loaded machines

                combined_score = (idle_time_weight * idle_time_score +
                                  remaining_ops_weight * remaining_ops_score +
                                  load_weight * load_score)
                
                if start_time < best_start_time:
                  best_start_time = start_time
                  best_operation = (job_id, op_idx)
                  best_machine = (machine, processing_time)

        job_id, op_idx = best_operation
        machine, processing_time = best_machine

        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        job_last_machine[job_id] = machine
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    return schedule
