
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that prioritizes minimizing makespan
    by selecting machines with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    for job_id in jobs:
        schedule[job_id] = []
        job = jobs[job_id]

        for op_idx, operation in enumerate(job):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines.
            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the selected machine.
            start_time = best_start_time
            end_time = start_time + best_processing_time
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

    return schedule
