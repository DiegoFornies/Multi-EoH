
def heuristic(input_data):
    """Combines shortest processing time and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    eligible_operations = {}
    for job_id, operations in jobs.items():
        eligible_operations[job_id] = 0

    scheduled_operations = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_operations < total_operations:
        available_operations = []
        for job_id, op_index in eligible_operations.items():
            if op_index < len(jobs[job_id]):
                available_operations.append((job_id, op_index))

        if not available_operations:
            break

        best_operation = None
        best_machine = None
        earliest_start_time = float('inf')
        shortest_processing_time = float('inf')
        least_loaded_machine_time = float('inf')

        for job_id, op_index in available_operations:
            machines, times = jobs[job_id][op_index]

            # Find the machine with the earliest available time AND least load
            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                processing_time = times[i]

                # Prioritize machines with less load considering ties with processing time.
                if machine_available_time[machine] < least_loaded_machine_time or (machine_available_time[machine] == least_loaded_machine_time and processing_time < shortest_processing_time):
                    least_loaded_machine_time = machine_available_time[machine]
                    shortest_processing_time = processing_time
                    earliest_start_time = start_time
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time


        if best_operation:
            job_id, op_index = best_operation
            machine = best_machine
            processing_time = best_processing_time
            start_time = best_start_time

            if job_id not in schedule:
                schedule[job_id] = []

            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time
            eligible_operations[job_id] += 1
            scheduled_operations += 1

    return schedule
