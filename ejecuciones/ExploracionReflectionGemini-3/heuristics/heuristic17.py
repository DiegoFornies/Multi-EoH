
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that prioritizes
    jobs with fewer remaining operations and selects machines with the earliest
    available time, considering both machine availability and job precedence.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    remaining_operations = {job: list(range(1, len(jobs_data[job]) + 1)) for job in range(1, n_jobs + 1)}
    schedule = {}

    completed_jobs = set()
    current_operations = {}
    for job in range(1, n_jobs + 1):
        current_operations[job] = 1
        schedule[job] = []

    while len(completed_jobs) < n_jobs:
        eligible_jobs = [job for job in range(1, n_jobs + 1) if job not in completed_jobs]

        if not eligible_jobs:
            break

        # Prioritize jobs with fewer remaining operations
        eligible_jobs.sort(key=lambda job: len(remaining_operations[job]))
        
        for job in eligible_jobs:
            if current_operations[job] is None:
                continue
            
            op_idx = current_operations[job] - 1
            machines, times = jobs_data[job][op_idx]

            # Find the machine with the earliest available time that can perform the operation
            best_machine, best_time = None, float('inf')
            for i, machine in enumerate(machines):
                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job])
                if start_time < best_time:
                    best_machine = machine
                    best_time = start_time
                    processing_time = times[i]

            start_time = best_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': current_operations[job],
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time
            remaining_operations[job].remove(current_operations[job])

            if not remaining_operations[job]:
                completed_jobs.add(job)
                current_operations[job] = None
            else:
                current_operations[job] += 1
    return schedule
