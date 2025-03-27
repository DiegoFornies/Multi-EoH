
def heuristic(input_data):
    """Greedy heuristic for FJSSP: Random machine selection with tie-breaking based on load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    import random

    job_ops = {job: 0 for job in jobs}
    job_order = list(jobs.keys())
    random.shuffle(job_order)


    for job in job_order:

        if job not in schedule:
            schedule[job] = []

        while job_ops[job] < len(jobs[job]):
            op_idx = job_ops[job]
            machines, times = jobs[job][op_idx]

            available_machines = []
            min_start_time = float('inf')
            best_machine = None
            best_time = None

            for m_idx, m in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_time[m], job_completion_time[job])
                end_time = start_time + processing_time

                available_machines.append((m, processing_time, start_time))

            if not available_machines:
                raise ValueError("No available machines for the current operation")

            # Tie-breaking: Random machine selection and machine load
            random.shuffle(available_machines)
            available_machines.sort(key=lambda x: (machine_load[x[0]]))  # Sort by load

            best_machine, best_time, start_time = available_machines[0]
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_time[best_machine] = end_time
            machine_load[best_machine] += best_time
            job_completion_time[job] = end_time

            job_ops[job] += 1

    return schedule
