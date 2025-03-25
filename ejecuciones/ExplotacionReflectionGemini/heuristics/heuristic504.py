
def heuristic(input_data):
    """Combines greedy makespan, SPT, and local search for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job_id: [] for job_id in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    available_operations = [(job_id, 0) for job_id in range(1, n_jobs + 1)]

    while available_operations:
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                #Machine load considered
                score = end_time + machine_load[machine]

                if score < earliest_end_time:
                    earliest_end_time = score
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        if best_operation:
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
            machine_load[machine] += processing_time
            available_operations.remove((job_id, op_idx))

            if op_idx + 1 < len(jobs[job_id]):
                available_operations.append((job_id, op_idx + 1))
    return schedule
