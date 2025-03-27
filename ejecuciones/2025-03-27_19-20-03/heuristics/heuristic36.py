
def heuristic(input_data):
    """Schedules jobs based on machine utilization."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_num in jobs:
        schedule[job_num] = []
        operations = jobs[job_num]

        for op_idx, op_data in enumerate(operations):
            eligible_machines = op_data[0]
            processing_times = op_data[1]

            best_machine = None
            min_machine_load = float('inf')

            for i, machine in enumerate(eligible_machines):
                if machine_load[machine] < min_machine_load:
                    min_machine_load = machine_load[machine]
                    best_machine = machine
                    best_processing_time = processing_times[i]

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
