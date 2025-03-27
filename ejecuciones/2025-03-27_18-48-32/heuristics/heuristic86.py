
def heuristic(input_data):
    """A heuristic for FJSSP: Earliest Due Date with machine consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_due_dates = {}  # Assign random due dates to jobs

    import random

    # Assign due dates for each job
    for job_id in jobs:
        total_processing_time = 0
        for operation in jobs[job_id]:
            total_processing_time += min(operation[1])  # Estimate processing time
        job_due_dates[job_id] = total_processing_time * (1 + random.uniform(0.5, 1.5))  # Due date

    job_ids = list(jobs.keys())
    job_ids.sort(key=lambda job_id: job_due_dates[job_id]) # Sort job by due date

    for job_id in job_ids:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            min_end_time = float('inf')

            # Choose the machine that minimizes the end time.
            for i, machine_id in enumerate(possible_machines):
                processing_time = possible_times[i]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, current_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_times[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[best_machine] = end_time
            current_time = end_time

    return schedule
