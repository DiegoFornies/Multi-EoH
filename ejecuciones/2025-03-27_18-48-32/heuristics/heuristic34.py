
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing machine idle time and balance workload.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    schedule = {}
    eligible_operations = []
    for job_id, operations in jobs_data.items():
        eligible_operations.append((job_id, 0))

    scheduled_operations = set()

    while eligible_operations:
        # Prioritize the machine with the earliest available time
        best_op = None
        earliest_end_time = float('inf')
        best_machine = None
        shortest_processing_time = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs_data[job_id][op_idx]

            # For each eligible operation, evaluate feasible machines.
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine]
                job_ready_time = job_completion_times[job_id]
                start_time = max(available_time, job_ready_time)
                end_time = start_time + processing_time

                if end_time < earliest_end_time :
                    earliest_end_time = end_time
                    best_op = (job_id, op_idx, machine, processing_time, start_time)
                    best_machine = machine
                    shortest_processing_time = processing_time

        if best_op is None:
            break

        job_id, op_idx, machine, processing_time, start_time = best_op

        if job_id not in schedule:
            schedule[job_id] = []

        op_num = op_idx + 1
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })

        machine_available_times[machine] = start_time + processing_time
        job_completion_times[job_id] = start_time + processing_time

        eligible_operations.remove((job_id, op_idx))

        next_op_idx = op_idx + 1
        if next_op_idx < len(jobs_data[job_id]):
            eligible_operations.append((job_id, next_op_idx))

    return schedule
