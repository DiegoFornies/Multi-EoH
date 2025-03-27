
def heuristic(input_data):
    """Schedules jobs balancing SPT and machine load dynamically."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    remaining_operations = {job: [(i + 1, op) for i, op in enumerate(jobs[job])] for job in range(1, n_jobs + 1)}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, ops in remaining_operations.items():
            if ops:
                eligible_operations.append((job, ops[0]))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        best_start_time = float('inf')

        for job, (op_num, (machines, times)) in eligible_operations:
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                # Dynamically adjust priority based on machine load
                load_factor = machine_load[machine] / (sum(machine_load.values()) + 1e-6) if sum(machine_load.values()) > 0 else 0
                priority = start_time + load_factor * processing_time  # Balance start time and load

                if priority < best_start_time:
                    best_start_time = priority
                    best_operation = (job, (op_num, (machines, times)))
                    best_machine = machine
                    best_processing_time = processing_time

        if best_operation is not None and best_machine is not None:
            job, (op_num, (machines, times)) = best_operation
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job] = end_time
            remaining_operations[job].pop(0)

    return schedule
