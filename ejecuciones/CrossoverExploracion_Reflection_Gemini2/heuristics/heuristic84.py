
def heuristic(input_data):
    """Combines SPT, machine load, and fewer machine options for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    machine_load = {m: 0 for m in range(n_machines)}
    next_operation = {job_id: 0 for job_id in jobs_data}

    def calculate_priority(job_id, op_idx, machines, times):
        """Calculates priority based on SPT, machine load, and machine count."""
        min_time = min(times)
        machine_count = len(machines)
        total_load = sum(machine_load[m] for m in machines)
        return min_time + 0.1 * total_load / machine_count + 0.01 * machine_count

    while True:
        eligible_operations = []
        for job_id in jobs_data:
            op_idx = next_operation[job_id]
            if op_idx >= len(jobs_data[job_id]):
                continue
            machines, times = jobs_data[job_id][op_idx]
            eligible_operations.append((job_id, op_idx, machines, times))

        if not eligible_operations:
            break

        if not eligible_operations:
            break

        best_op = None
        best_machine = None
        min_start_time = float('inf')
        processing_time = 0

        eligible_operations.sort(key=lambda x: calculate_priority(x[0], x[1], x[2], x[3]))

        job_id, op_idx, machines, times = eligible_operations[0]
        min_load = float('inf')
        selected_machine = None
        selected_processing_time = 0

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            if machine_load[machine] < min_load:
                min_load = machine_load[machine]
                selected_machine = machine
                selected_processing_time = times[m_idx]

        start_time = max(machine_available_time[selected_machine], job_completion_time[job_id])
        end_time = start_time + selected_processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': selected_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': selected_processing_time
        })

        machine_available_time[selected_machine] = end_time
        job_completion_time[job_id] = end_time
        machine_load[selected_machine] += selected_processing_time
        next_operation[job_id] += 1

    return schedule
