
def heuristic(input_data):
    """Earliest Due Date (EDD) based heuristic for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Calculate job due dates (sum of processing times)
    job_due_dates = {}
    for job_id in range(1, n_jobs + 1):
        due_date = 0
        for operation_data in jobs[job_id]:
            due_date += min(operation_data[1])  # Use shortest processing time
        job_due_dates[job_id] = due_date

    # Sort jobs by due date (EDD)
    sorted_jobs = sorted(job_due_dates.items(), key=lambda item: item[1])

    for job_id, _ in sorted_jobs:
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for op_idx, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]
            op_num = op_idx + 1

            best_machine = None
            min_completion_time = float('inf')

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_completion_time:
                    min_completion_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
