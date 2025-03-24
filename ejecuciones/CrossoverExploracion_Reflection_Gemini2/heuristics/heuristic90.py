
def heuristic(input_data):
    """Combines SPT, least loaded machine, & job priority for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data.keys()}
    schedule = {j: [] for j in jobs_data.keys()}
    remaining_operations = {j: len(jobs_data[j]) for j in jobs_data.keys()}

    def calculate_priority(job):
      total_processing_time = 0
      for op_idx in range(len(jobs_data[job])):
          machines, times = jobs_data[job][op_idx]
          total_processing_time += min(times)
      return total_processing_time

    job_priority = sorted(jobs_data.keys(), key=calculate_priority)

    while any(remaining_operations.values()):
        eligible_jobs = [job for job in job_priority if remaining_operations[job] > 0]

        best_job = None
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for job in eligible_jobs:
            op_idx = len(schedule.get(job, []))
            machines, processing_times = jobs_data[job][op_idx]
            
            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                cost = start_time + processing_time + machine_load[machine]

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_job = job
                    best_machine = machine
                    best_processing_time = processing_time
        
        if best_job is None:
            break

        op_idx = len(schedule.get(best_job, [])) + 1
        start_time = best_start_time
        end_time = start_time + best_processing_time

        if best_job not in schedule:
            schedule[best_job] = []
            
        schedule[best_job].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[best_job] = end_time
        machine_load[best_machine] += best_processing_time
        remaining_operations[best_job] -= 1

    return schedule
