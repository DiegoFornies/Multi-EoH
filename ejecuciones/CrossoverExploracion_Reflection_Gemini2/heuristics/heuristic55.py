
def heuristic(input_data):
    """A greedy heuristic for FJSSP, prioritizing minimizing makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_last_end = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            operations.append((job, op_idx, machines, times))

    while operations:
        best_op = None
        best_machine = None
        min_end_time = float('inf')

        for job, op_idx, machines, times in list(operations):
            available_machines = jobs_data[job][op_idx][0]
            processing_times = jobs_data[job][op_idx][1]

            for m_idx, machine in enumerate(available_machines):
                start_time = max(machine_available[machine], job_last_end[job])
                end_time = start_time + processing_times[m_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job, op_idx, machines, times)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_times[m_idx]

        job, op_idx, machines, times = best_op
        op_num = op_idx + 1
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available[best_machine] = best_start_time + best_processing_time
        job_last_end[job] = best_start_time + best_processing_time

        operations.remove(best_op)

    return schedule
