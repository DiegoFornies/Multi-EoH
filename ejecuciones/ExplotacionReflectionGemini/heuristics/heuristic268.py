
def heuristic(input_data):
    """Combines SPT and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    available_operations = []
    for job_id in jobs:
        available_operations.append((job_id, 1))

    while available_operations:
        best_op = None
        min_score = float('inf')

        for job_id, op_num in available_operations:
            machines, times = jobs[job_id][op_num - 1]

            for m_idx, m in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_times[m], job_completion_times[job_id] if op_num > 1 else 0)
                end_time = start_time + processing_time

                # Prioritize SPT & balance machine load.
                score = processing_time + machine_load[m] * 0.05 

                if score < min_score:
                    min_score = score
                    best_op = (job_id, op_num, m, start_time, processing_time)

        if best_op:
            job_id, op_num, assigned_machine, start_time, processing_time = best_op
            end_time = start_time + processing_time

            if job_id not in schedule:
                schedule[job_id] = []
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[assigned_machine] = end_time
            job_completion_times[job_id] = end_time
            machine_load[assigned_machine] += processing_time

            available_operations.remove((job_id, op_num))

            if op_num < len(jobs[job_id]):
                available_operations.append((job_id, op_num + 1))

    return schedule
