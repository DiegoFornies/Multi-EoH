
def heuristic(input_data):
    """
    A heuristic for the FJSSP that considers machine load and job completion time.
    Schedules operations based on earliest completion time across feasible machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_loads = {m: 0 for m in range(n_machines)}  # Track machine utilization

    schedule = {}
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    operations = [] #collect operations from all jobs for sorting
    for job_id, operations_list in jobs_data.items():
        for op_idx, op_data in enumerate(operations_list):
            operations.append((job_id, op_idx, op_data))

    #sort operations from the smallest number of machines available to the largest. First operation
    #of each job is given higher priority. This is a way to prioritize critical operations and sequence
    #them without breaking feasibility constraints.
    operations.sort(key=lambda x: (x[1]!=0, len(x[2][0])))


    for job_id, op_idx, op_data in operations:
        machines, times = op_data
        op_num = op_idx + 1

        best_machine = None
        earliest_completion_time = float('inf')
        processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time_candidate = times[m_idx]

            start_time_candidate = max(machine_available_times[machine], job_completion_times[job_id])
            completion_time_candidate = start_time_candidate + processing_time_candidate

            if completion_time_candidate < earliest_completion_time:
                earliest_completion_time = completion_time_candidate
                best_machine = machine
                processing_time = processing_time_candidate

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_loads[best_machine] += processing_time

    return schedule
