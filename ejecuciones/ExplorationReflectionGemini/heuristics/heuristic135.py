
def heuristic(input_data):
    """Schedules jobs based on earliest due date and least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    job_due_dates = {job: len(jobs[job]) * 10 for job in range(1, n_jobs + 1)} #Initial estimate

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_completion_time = float('inf')
            
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_load[machine], job_completion_time[job])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time
    
    # Sort jobs by due date, shortest first
    sorted_jobs = sorted(jobs.keys(), key=lambda job: job_due_dates[job])
    
    final_schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job in sorted_jobs:
        final_schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_completion_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_load[machine], job_completion_time[job])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            final_schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time

    return final_schedule
