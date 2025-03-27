
def heuristic(input_data):
    """Earliest Due Date (EDD) dispatching rule."""
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    n_jobs = input_data['n_jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {}

    # Calculate job due dates based on total processing time.
    job_due_dates = {}
    for job_id in range(1, n_jobs + 1):
        total_processing_time = 0
        for op_data in jobs_data[job_id]:
            total_processing_time += min(op_data[1])
        job_due_dates[job_id] = total_processing_time

    # Sort jobs by due date (EDD).
    sorted_jobs = sorted(job_due_dates.items(), key=lambda item: item[1])

    for job_id, _ in sorted_jobs:
        schedule[job_id] = []
        operations = jobs_data[job_id]

        for op_idx, op_data in enumerate(operations):
            machines, processing_times = op_data
            op_num = op_idx + 1

            # Find the machine that allows earliest start.
            best_machine = None
            min_start_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_times[machine_idx]

            start_time = min_start_time
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
