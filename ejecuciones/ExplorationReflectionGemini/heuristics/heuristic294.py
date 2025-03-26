
def heuristic(input_data):
    """Earliest Due Date (EDD) scheduling with machine consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    job_due_dates = {} #Estimate job due dates.

    # Estimate due dates (sum of processing times)
    for job_id in range(1, n_jobs + 1):
        total_processing_time = 0
        for operation_data in jobs[job_id]:
            total_processing_time += min(operation_data[1]) # Use shortest time if multiple options
        job_due_dates[job_id] = total_processing_time * 2 # Due date twice processing time.

    # Sort jobs by due date
    sorted_jobs = sorted(job_due_dates.items(), key=lambda item: item[1])

    for job_id, _ in sorted_jobs:
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Find machine that allows earliest finish
            best_machine = None
            earliest_finish = float('inf')
            best_processing_time = None

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_finish:
                    earliest_finish = end_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule operation
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job states
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
