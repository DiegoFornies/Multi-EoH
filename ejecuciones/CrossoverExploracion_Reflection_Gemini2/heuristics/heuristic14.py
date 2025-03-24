
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing machine idle time
    and balancing machine load, considering operation feasibility and sequencing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    machine_assignments = {j: [] for j in jobs}  # Store machine assignments for each job
    schedule = {}

    # Prioritize operations based on shortest processing time first (SPT) among feasible machines.
    for job in jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine with the shortest available time that is feasible for this operation.
            best_machine = None
            min_end_time = float('inf')
            best_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = available_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_time = processing_time

            if best_machine is not None:
                start_time = max(machine_available_time[best_machine], job_completion_time[job])
                end_time = start_time + best_time
                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_time
                })
                machine_assignments[job].append(best_machine)  # Store the assignment
                machine_available_time[best_machine] = end_time
                job_completion_time[job] = end_time
            else:
                 print("No valid machine found for operation!")
                 return None
    return schedule
