
def heuristic(input_data):
    """
    Schedules jobs using a priority-based earliest due date (EDD) and
    least loaded machine, balancing makespan and machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_priority = {j: len(jobs[j]) for j in range(1, n_jobs + 1)} # Job with the most operations gets higher priority.

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    remaining_operations = {job_id: [(i + 1, op) for i, op in enumerate(jobs[job_id])] for job_id in range(1, n_jobs + 1)}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job_id in range(1, n_jobs + 1):
            if remaining_operations[job_id]:
                eligible_operations.append((job_id, remaining_operations[job_id][0]))

        # Sort eligible operations by EDD (job_priority)
        eligible_operations.sort(key=lambda x: (job_priority[x[0]], x[1][0]))

        for job_id, (op_num, op_data) in eligible_operations:
            machines, times = op_data

            # Find the least loaded machine among feasible machines.
            best_machine = None
            min_machine_load = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                machine_load = machine_available_time[machine]

                if machine_load < min_machine_load:
                    min_machine_load = machine_load
                    best_machine = machine
                    best_processing_time = processing_time

            if best_machine is not None:
                start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
                end_time = start_time + best_processing_time

                schedule[job_id].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })

                machine_available_time[best_machine] = end_time
                job_completion_time[job_id] = end_time
                remaining_operations[job_id].pop(0)
            else:
                print(f"Warning: No suitable machine found for job {job_id}, operation {op_num}")
                return None

    return schedule
