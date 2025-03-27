
def heuristic(input_data):
    """
    FJSSP heuristic: SPT-LPT (Shortest Processing Time - Least Processing Time)
    SPT within a job, LPT across jobs, focusing on reducing makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs.items()}

    # Sort jobs by total processing time in descending order (LPT)
    job_processing_times = {}
    for job, operations in jobs.items():
        total_time = 0
        for op_idx, operation in enumerate(operations):
            min_time = min(operation[1])
            total_time += min_time
        job_processing_times[job] = total_time

    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1], reverse=True)
    sorted_job_ids = [job_id for job_id, _ in sorted_jobs]

    while any(remaining_operations.values()):
        eligible_operations = []
        for job in sorted_job_ids:
            if job in remaining_operations and remaining_operations[job]:
                op_num = remaining_operations[job][0]
                machines, times = jobs[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Select the operation with the shortest processing time (SPT)
        best_operation = None
        min_processing_time = float('inf')

        for job, op_num, machines, times in eligible_operations:
            shortest_time = min(times)
            if shortest_time < min_processing_time:
                min_processing_time = shortest_time
                best_operation = (job, op_num, machines, times)

        if best_operation:
            job, op_num, machines, times = best_operation

            # Choose the machine that allows for the earliest start time
            best_machine = None
            earliest_start_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_processing_time = times[m_idx]

            start_time = earliest_start_time
            processing_time = best_processing_time
            machine = best_machine
           
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
