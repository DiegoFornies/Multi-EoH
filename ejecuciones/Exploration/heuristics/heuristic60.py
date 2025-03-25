
def heuristic(input_data):
    """Schedules jobs to minimize makespan,separation, and balance via SPT and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_end_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs.items()}

    while any(remaining_operations[job] for job in jobs):
        eligible_operations = []
        for job in jobs:
            if remaining_operations[job]:
                operation_number = remaining_operations[job][0]
                operation_index = operation_number - 1
                machines, times = jobs[job][operation_index]
                eligible_operations.append((job, operation_number, machines, times))

        # Prioritize by shortest processing time
        eligible_operations.sort(key=lambda x: min(x[3]))  # x[3] are times

        for job, operation_number, machines, times in eligible_operations:
            if operation_number not in remaining_operations[job]: #double check for possible race condition
              continue

            operation_index = operation_number - 1

            # Find the machine that allows the earliest completion time AND least loaded
            best_machine, best_start_time, best_end_time, best_processing_time = None, float('inf'), float('inf'), None
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_end_time[job])
                end_time = start_time + processing_time

                if end_time < best_end_time:
                    best_machine, best_start_time, best_end_time, best_processing_time = machine, start_time, end_time, processing_time

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_end_time
            job_end_time[job] = best_end_time
            remaining_operations[job].pop(0)
    return schedule
