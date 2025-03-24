
def heuristic(input_data):
    """Schedules jobs using a combination of earliest start time and least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    next_ops = {}
    for j in jobs_data:
        next_ops[j] = 1

    def calculate_machine_load(machine):
        """Calculates the load on a given machine."""
        load = 0
        for job in schedule:
            for op in schedule[job]:
                if op['Assigned Machine'] == machine:
                    load += op['Processing Time']
        return load

    def get_available_ops():
        """Gets the available operations to schedule."""
        available_ops = []
        for job_id in jobs_data:
            if next_ops[job_id] <= len(jobs_data[job_id]):
                op_index = next_ops[job_id] - 1
                machines, times = jobs_data[job_id][op_index]
                available_ops.append((job_id, op_index, machines, times))
        return available_ops

    while True:
        available_ops = get_available_ops()
        if not available_ops:
            break

        best_op = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_index, machines, times in available_ops:
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                machine_load = calculate_machine_load(machine)

                if end_time + machine_load < min_end_time: #consider machine_load as tiebreaker
                    min_end_time = end_time + machine_load
                    best_op = (job_id, op_index, machines, times)
                    best_machine = machine

        job_id, op_index, machines, times = best_op
        processing_time = times[machines.index(best_machine)]
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id] = schedule.get(job_id, []) + [{
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        }]

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        next_ops[job_id] += 1

    return schedule
