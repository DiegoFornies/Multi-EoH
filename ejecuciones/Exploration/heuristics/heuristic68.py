
def heuristic(input_data):
    """Combines SPT, EDD, and earliest available machine for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    job_due_dates = {}

    # Estimate due dates based on total processing time.
    for job_id in jobs:
        total_processing_time = sum(min(op[1]) for op in jobs[job_id])
        job_due_dates[job_id] = total_processing_time * 2

    # Sort jobs based on EDD.
    sorted_jobs = sorted(jobs.keys(), key=lambda job_id: job_due_dates[job_id])

    for job_id in sorted_jobs:
        schedule[job_id] = []
        for operation_index, operation in enumerate(jobs[job_id]):
            machines = operation[0]
            processing_times = operation[1]

            # SPT and earliest machine: choose the best machine
            best_machine = None
            min_end_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_times[i]

            # Schedule the operation
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
