
def heuristic(input_data):
    """Combines shortest processing time and machine load for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Prioritize operations: Shortest processing time on least loaded machine
        best_op = None
        best_job = None
        best_machine = None
        min_end_time = float('inf')

        for job, op_num, machines, times in eligible_operations:
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + times[m_idx]
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = op_num
                    best_job = job
                    best_machine = machine
                    processing_time = times[m_idx]

        start_time = max(machine_available_time[best_machine], job_completion_time[best_job])

        if best_job not in schedule:
            schedule[best_job] = []

        schedule[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = start_time + processing_time
        job_completion_time[best_job] = start_time + processing_time

        remaining_operations[best_job].pop(0)

    return schedule
