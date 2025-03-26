
def heuristic(input_data):
    """Schedules jobs considering machine load and operation urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    def calculate_urgency(job_id, operation_index):
        """Estimates the urgency of an operation."""
        remaining_operations = len(jobs[job_id]) - operation_index
        return remaining_operations # Basic urgency: ops left

    for job_id in range(1, n_jobs + 1):
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            best_end_time = float('inf')

            urgency = calculate_urgency(job_id, operation_index) # Calculate job's urgency

            for machine_index, machine in enumerate(possible_machines):
                processing_time = possible_times[machine_index]
                start_time = max(machine_load[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                # Choose machine with shortest completion time adjusted by job urgency
                if end_time - urgency * 0.01 < best_end_time: # Apply urgency
                    best_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_load[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
