
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes earliest available machine."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for operation_index, operation in enumerate(operations):
            machines, processing_times = operation
            operation_number = operation_index + 1

            # Find the earliest available machine among options
            best_machine = None
            earliest_start_time = float('inf')
            best_processing_time = None

            for machine_index, machine in enumerate(machines):
                processing_time = processing_times[machine_index]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the selected machine
            start_time = earliest_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
