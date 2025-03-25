
def heuristic(input_data):
    """Schedules jobs using a machine load balancing heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        job_operations = jobs[job_id]
        job_completion_time = 0

        for operation_index, operation in enumerate(job_operations):
            possible_machines = operation[0]
            possible_times = operation[1]
            operation_number = operation_index + 1

            # Choose machine with the lowest current load
            best_machine = possible_machines[0]
            min_load = float('inf')

            for i, machine in enumerate(possible_machines):
                if machine_load[machine] < min_load:
                    min_load = machine_load[machine]
                    best_machine = machine

            # Get processing time for the selected machine
            processing_time = possible_times[possible_machines.index(best_machine)]

            # Schedule the operation
            start_time = max(machine_available_time[best_machine], job_completion_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time = end_time

    return schedule
