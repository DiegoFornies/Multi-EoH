
def heuristic(input_data):
    """FJSSP heuristic: Combines EDD and machine load for balanced scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Prioritize based on a combination of factors
        best_op = None
        best_machine = None
        best_start_time = float('inf')
        best_job = None
        best_processing_time = None
        for job, op_num, machines, times in eligible_operations:
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                # Calculate a priority score (lower is better)
                load_penalty = machine_load[machine] * 0.1  # Adjust the weight
                urgency_bonus = job_completion_time[job] * 0.05 #Adjust the weight

                score = start_time + load_penalty - urgency_bonus

                if score < best_start_time:
                    best_start_time = score
                    best_op = op_num
                    best_machine = machine
                    best_job = job
                    best_processing_time = processing_time

        start_time = max(machine_available_time[best_machine], job_completion_time[best_job])

        if best_job not in schedule:
            schedule[best_job] = []

        schedule[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = start_time + best_processing_time
        job_completion_time[best_job] = start_time + best_processing_time
        machine_load[best_machine] += best_processing_time

        remaining_operations[best_job].pop(0)

    return schedule
