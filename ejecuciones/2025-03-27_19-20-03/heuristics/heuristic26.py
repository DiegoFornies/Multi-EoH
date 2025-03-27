
def heuristic(input_data):
    """Schedules jobs minimizing makespan using earliest start time based on machine availability and job dependencies."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Sort operations of all jobs based on the shortest processing time among possible machines
    eligible_operations = []
    for job_id, operations in jobs.items():
        for op_idx, operation in enumerate(operations):
            machines = operation[0]
            times = operation[1]
            min_time = float('inf')
            best_machine = None
            for i in range(len(machines)):
                if times[i] < min_time:
                    min_time = times[i]
                    best_machine = machines[i]
            eligible_operations.append((job_id, op_idx + 1, best_machine, min_time, machines, times))

    # Sort based on shortest processing time first.
    eligible_operations = sorted(eligible_operations, key=lambda x: x[3])

    scheduled_operations = set()

    while eligible_operations:
        # Prioritize jobs that has less slack (estimated end time - job_completion_time).
        eligible_operations = sorted(eligible_operations, key=lambda x: machine_available_time[x[2]] + x[3] - job_completion_time[x[0]])

        job_id, op_num, machine, processing_time, machines_list, times_list = eligible_operations.pop(0)

        machine_index = machines_list.index(machine)
        processing_time = times_list[machine_index]
        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
