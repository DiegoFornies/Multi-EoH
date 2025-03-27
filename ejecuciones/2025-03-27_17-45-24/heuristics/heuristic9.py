
def heuristic(input_data):
    """
    Heuristic for FJSSP:
    1. Prioritize jobs with fewer operations.
    2. Assign operations to machines with the earliest available time (Earliest Finish Time - EFT).
    3. Break ties randomly.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Sort jobs by number of operations (shortest job first)
    job_order = sorted(jobs_data.keys(), key=lambda job: len(jobs_data[job]))

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data.keys()}
    schedule = {job: [] for job in jobs_data.keys()}

    import random

    for job in job_order:
        operations = jobs_data[job]

        for op_idx, (machines, times) in enumerate(operations):
            op_num = op_idx + 1

            # Find the machine with the Earliest Finish Time (EFT)
            efts = {}
            for machine_idx, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job])
                eft = start_time + times[machine_idx]
                efts[machine] = (start_time, eft, times[machine_idx])

            best_machines = [m for m in efts if efts[m][1] == min(efts[m][1] for m in efts)]

            # Randomly select one machine if there is more than one
            assigned_machine = random.choice(best_machines)

            start_time, end_time, processing_time = efts[assigned_machine]
            # Update schedule
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_available_times[assigned_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
