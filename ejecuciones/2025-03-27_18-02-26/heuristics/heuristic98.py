
def heuristic(input_data):
    """Schedules operations based on earliest finish time."""
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {job: 0 for job in jobs_data}
    schedule = {}

    for job_id, operations in jobs_data.items():
        schedule[job_id] = []
        for op_idx, op_data in enumerate(operations):
            machines, processing_times = op_data
            op_num = op_idx + 1
            best_machine, min_finish_time, best_ptime = None, float('inf'), None

            for i, machine in enumerate(machines):
                start_time = max(machine_available[machine], job_completion[job_id])
                finish_time = start_time + processing_times[i]
                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = machine
                    best_ptime = processing_times[i]

            start_time = max(machine_available[best_machine], job_completion[job_id])
            end_time = start_time + best_ptime

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_ptime
            })

            machine_available[best_machine] = end_time
            job_completion[job_id] = end_time

    return schedule
