
def heuristic(input_data):
    """
    A heuristic for FJSSP that considers machine load and job priority.
    Prioritize jobs with more operations.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_priority = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort jobs based on priority (number of operations)
    sorted_jobs = sorted(job_priority.items(), key=lambda item: item[1], reverse=True)

    for job_num, _ in sorted_jobs:
        schedule[job_num] = []
        operations = jobs[job_num]

        for op_idx, operation in enumerate(operations):
            machines, times = operation

            best_machine = -1
            min_expected_load = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                expected_load = machine_load[machine] + processing_time

                if expected_load < min_expected_load:
                    min_expected_load = expected_load
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_load[best_machine], job_completion_time[job_num])
            end_time = start_time + best_processing_time
            
            schedule[job_num].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = end_time
            job_completion_time[job_num] = end_time

    return schedule
