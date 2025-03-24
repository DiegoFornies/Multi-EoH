
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes operations with fewer machine options
    and shorter processing times to balance machine load and minimize makespan.
    """
    schedule = {}
    machine_time = {m: 0 for m in range(input_data['n_machines'])}
    job_time = {j: 0 for j in input_data['jobs']}

    # Create a list of operations with job, operation index, and machine/time options
    operations = []
    for job, ops in input_data['jobs'].items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by the number of available machines (fewer first)
    operations.sort(key=lambda x: len(x[2]))

    while operations:
        best_op = None
        best_machine = None
        min_end_time = float('inf')

        for job, op_idx, machines, times in operations:
            best_local_machine = None
            min_local_end = float('inf')

            for m_idx, m in enumerate(machines):
                start_time = max(machine_time[m], job_time[job])
                end_time = start_time + times[m_idx]

                if end_time < min_local_end:
                    min_local_end = end_time
                    best_local_machine = m

            if min_local_end < min_end_time:
                min_end_time = min_local_end
                best_op = (job, op_idx, machines, times)
                best_machine = best_local_machine

        job, op_idx, machines, times = best_op
        op_num = op_idx + 1
        m_idx = machines.index(best_machine)
        processing_time = times[m_idx]
        
        start_time = max(machine_time[best_machine], job_time[job])
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_time[best_machine] = end_time
        job_time[job] = end_time

        operations.remove((job, op_idx, machines, times))

    return schedule
