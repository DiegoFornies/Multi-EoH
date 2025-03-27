
def heuristic(input_data):
    """
    Heuristic for FJSSP that minimizes makespan by prioritizing operations
    with the shortest processing time available on the least loaded machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Select the operation with the shortest processing time on the least loaded machine
        best_operation = None
        best_makespan = float('inf')

        for job, op_num, machines, times in eligible_operations:
            possible_makespans = []
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])
                end_time = start_time + times[m_idx]
                possible_makespans.append((end_time, m, start_time, times[m_idx]))

            #Find the option with min finish time, breaking ties with least loaded machine
            min_end_time = min(possible_makespans, key=lambda x: (x[0]))
            
            if min_end_time[0] < best_makespan:
                best_makespan = min_end_time[0]
                best_operation = (job, op_num, min_end_time[1], min_end_time[2], min_end_time[3])
            elif min_end_time[0] == best_makespan:
                if machine_available_time[min_end_time[1]] < machine_available_time[best_operation[2]]:
                    best_operation = (job, op_num, min_end_time[1], min_end_time[2], min_end_time[3])

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
