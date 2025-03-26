
def heuristic(input_data):
    """Schedules jobs considering operation urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of all operations with urgency (SPT-like)
    operations = []
    for job_id in range(1, n_jobs + 1):
        for operation_index, operation_data in enumerate(jobs[job_id]):
            machines = operation_data[0]
            times = operation_data[1]
            min_time = min(times)  # Urgency based on shortest processing time
            operations.append((min_time, job_id, operation_index, machines, times))

    # Sort operations by urgency (shortest processing time first)
    operations.sort()

    for urgency, job_id, operation_index, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')

        # Find the machine that results in the earliest completion time
        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]

            start_time = max(machine_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        machine_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

    return schedule
