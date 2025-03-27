
def heuristic(input_data):
    """Schedules jobs by Shortest Processing Time (SPT) and Earliest Due Date (EDD)."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    # Assign a virtual due date to each job: sum of processing times
    job_due_dates = {}
    for job in range(1, n_jobs + 1):
        total_processing_time = 0
        for op_num in range(1, len(jobs_data[job]) + 1):
            machines, times = jobs_data[job][op_num - 1]
            total_processing_time += min(times)  # Shortest processing time
        job_due_dates[job] = total_processing_time

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # SPT within EDD
        best_operation = None
        best_priority = float('inf')

        for job, op_num, machines, times in eligible_operations:
            min_time = float('inf')
            best_machine_for_op = None
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])
                if times[m_idx] < min_time:
                    min_time = times[m_idx]
                    best_machine_for_op = (m, start_time, times[m_idx])
            
            m, start_time, processing_time = best_machine_for_op

            # Priority: Due Date + SPT (shorter is better)
            priority = job_due_dates[job] + processing_time # EDD+SPT

            if priority < best_priority:
                best_priority = priority
                best_operation = (job, op_num, m, start_time, processing_time)

        if best_operation:
            job, op_num, machine, start_time, processing_time = best_operation

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = start_time + processing_time
            job_completion_time[job] = start_time + processing_time

            remaining_operations[job].pop(0)

    return schedule
