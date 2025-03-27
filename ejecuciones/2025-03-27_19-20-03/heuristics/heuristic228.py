
def heuristic(input_data):
    """Schedules jobs using a modified shortest processing time (SPT) and earliest due date (EDD) approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_work = {}

    for job in jobs:
        total_time = sum(min(times) for machines, times in jobs[job])
        job_remaining_work[job] = total_time

    job_order = sorted(jobs.keys(), key=lambda job: (job_remaining_work[job], job))

    for job in job_order:
        schedule[job] = []
        current_op = 0

        while current_op < len(jobs[job]):
            machines, times = jobs[job][current_op]
            best_machine = None
            min_end_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[job])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = times[i]

            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': current_op + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time
            job_remaining_work[job] -= best_processing_time
            current_op += 1

    return schedule
