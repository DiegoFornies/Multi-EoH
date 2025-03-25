
def heuristic(input_data):
    """
    A heuristic algorithm for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes operations with the shortest processing time on available machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    eligible_operations = {}
    for job_id in jobs_data:
        eligible_operations[job_id] = 0
    
    completed_operations = {job_id: [] for job_id in jobs_data}

    def get_eligible_operations():
        eligible = []
        for job_id, op_index in eligible_operations.items():
            if op_index < len(jobs_data[job_id]):
                eligible.append((job_id, op_index))
        return eligible

    def find_best_machine(job_id, op_index):
        machines, times = jobs_data[job_id][op_index]
        best_machine, best_time = None, float('inf')

        for i, machine in enumerate(machines):
            time = times[i]
            available_time = max(machine_available_time[machine], job_completion_time[job_id])
            if available_time + time < best_time:
                best_time = available_time + time
                best_machine = machine
                best_processing_time = time
        return best_machine, best_processing_time

    while True:
        eligible = get_eligible_operations()
        if not eligible:
            break

        best_job, best_op = None, None
        earliest_end_time = float('inf')
        chosen_machine = None
        chosen_processing_time = None

        for job_id, op_index in eligible:
            machine, processing_time = find_best_machine(job_id, op_index)
            available_time = max(machine_available_time[machine], job_completion_time[job_id])

            if available_time + processing_time < earliest_end_time:
                earliest_end_time = available_time + processing_time
                best_job = job_id
                best_op = op_index
                chosen_machine = machine
                chosen_processing_time = processing_time

        start_time = max(machine_available_time[chosen_machine], job_completion_time[best_job])
        end_time = start_time + chosen_processing_time

        op_num = best_op + 1

        if best_job not in schedule:
            schedule[best_job] = []

        schedule[best_job].append({
            'Operation': op_num,
            'Assigned Machine': chosen_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': chosen_processing_time
        })

        machine_available_time[chosen_machine] = end_time
        job_completion_time[best_job] = end_time
        eligible_operations[best_job] += 1
    return schedule
