
def heuristic(input_data):
    """Heuristic for FJSSP: Prioritizes operations with fewer machine options and uses a machine load balancing strategy."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    machine_load = {m: 0 for m in range(n_machines)}

    next_operation = {job_id: 0 for job_id in jobs_data}
    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs_data.values()):
        eligible_operations = []
        for job_id in jobs_data:
            op_idx = next_operation[job_id]
            if op_idx >= len(jobs_data[job_id]):
                continue

            machines, times = jobs_data[job_id][op_idx]
            eligible_operations.append((job_id, op_idx, machines, times))

        if not eligible_operations:
            break

        # Prioritize operations with fewer machine options
        eligible_operations.sort(key=lambda x: len(x[2])) #Sort by number of possible machines

        best_op = None
        best_machine = None
        earliest_start = float('inf')
        processing_time = 0

        for job_id, op_idx, machines, times in eligible_operations:
            #Find the machine with minimum load
            min_load = float('inf')
            selected_machine = None
            selected_processing_time = 0

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if machine_load[machine] < min_load:
                   min_load = machine_load[machine]
                   selected_machine = machine
                   selected_processing_time = times[m_idx]
            
            start_time = max(machine_available_times[selected_machine], job_completion_times[job_id])

            if start_time < earliest_start:
                earliest_start = start_time
                best_op = (job_id, op_idx, machines, times)
                best_machine = selected_machine
                processing_time = selected_processing_time

        if best_op is None:
            break

        job_id, op_idx, machines, times = best_op
        op_num = op_idx + 1

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
        machine_load[best_machine] += processing_time
        scheduled_operations.add((job_id, op_idx))
        next_operation[job_id] += 1

    return schedule
