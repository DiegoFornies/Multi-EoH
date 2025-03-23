
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules operations greedily, prioritizing shortest processing time
    on the least loaded machine, considering job dependencies.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times

    for job_id in jobs:
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, op_data in enumerate(operations):
            machines, times = op_data
            op_num = op_idx + 1

            # Find the machine with the earliest available time and shortest processing time
            best_machine, best_time = None, float('inf')
            for m_idx, machine in enumerate(machines):
                if times[m_idx] < best_time:
                    if max(machine_available_time[machine], job_completion_time[job_id]) + times[m_idx] < best_time + max(machine_available_time[machine], job_completion_time[job_id]):
                         best_machine = machine
                         best_time = times[m_idx]

            # Schedule the operation on the selected machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id]) # consider job dependencies
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
