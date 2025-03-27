
def heuristic(input_data):
    """Schedules FJSSP jobs minimizing makespan using SPT and random machine selection."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    import random

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    job_next_operation = {job: 0 for job in range(1, n_jobs + 1)}

    scheduled_count = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_count < total_operations:
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if job_next_operation[job] < len(jobs[job]):
                eligible_operations.append(job)

        if not eligible_operations:
            break

        # SPT: Shortest Processing Time first
        shortest_job = min(eligible_operations, key=lambda job: min(jobs[job][job_next_operation[job]][1])) #minimum processing time
        op_index = job_next_operation[shortest_job]
        machines, times = jobs[shortest_job][op_index]

        # Random machine Selection
        available_machines = []
        for machine, time in zip(machines, times):
            available_machines.append((machine,time))

        selected_machine_index = random.randint(0, len(available_machines)-1)
        best_machine = available_machines[selected_machine_index][0]
        best_processing_time = available_machines[selected_machine_index][1]

        start_time = max(machine_available_time[best_machine], job_completion_time[shortest_job])
        operation = {
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': start_time + best_processing_time,
            'Processing Time': best_processing_time
        }
        schedule[shortest_job].append(operation)

        machine_available_time[best_machine] = start_time + best_processing_time
        job_completion_time[shortest_job] = start_time + best_processing_time
        job_next_operation[shortest_job] += 1
        scheduled_count += 1

    return schedule
