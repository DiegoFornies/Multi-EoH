
def heuristic(input_data):
    """Heuristic for FJSSP: Random assignment with iterative improvement."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    def initial_schedule():
        schedule = {}
        for job in jobs:
            schedule[job] = []
            for op_idx, (machines, times) in enumerate(jobs[job]):
                machine_idx = random.randint(0, len(machines) - 1)
                schedule[job].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': machines[machine_idx],
                    'Processing Time': times[machine_idx]
                })
        return schedule

    def calculate_makespan(schedule):
        machine_end_times = {m: 0 for m in range(n_machines)}
        job_end_times = {j: 0 for j in range(1, n_jobs + 1)}
        for job in schedule:
            current_time = 0
            for op in schedule[job]:
                machine = op['Assigned Machine']
                processing_time = op['Processing Time']
                start_time = max(machine_end_times[machine], current_time)
                end_time = start_time + processing_time
                machine_end_times[machine] = end_time
                current_time = end_time
                job_end_times[job] = end_time
        return max(machine_end_times.values())

    def improve_schedule(schedule, iterations=100):
        best_schedule = schedule
        best_makespan = calculate_makespan(schedule)

        for _ in range(iterations):
            job = random.choice(list(jobs.keys()))
            op_idx = random.randint(0, len(jobs[job]) - 1)

            original_machine = best_schedule[job][op_idx]['Assigned Machine']
            original_processing_time = best_schedule[job][op_idx]['Processing Time']

            machines, times = jobs[job][op_idx]
            new_machine_idx = random.randint(0, len(machines) - 1)

            best_schedule[job][op_idx]['Assigned Machine'] = machines[new_machine_idx]
            best_schedule[job][op_idx]['Processing Time'] = times[new_machine_idx]
            new_makespan = calculate_makespan(best_schedule)

            if new_makespan < best_makespan:
                best_makespan = new_makespan
            else:
                best_schedule[job][op_idx]['Assigned Machine'] = original_machine
                best_schedule[job][op_idx]['Processing Time'] = original_processing_time

        return best_schedule

    initial = initial_schedule()
    improved = improve_schedule(initial)

    final_schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in improved:
        final_schedule[job] = []
        for op in improved[job]:
            machine = op['Assigned Machine']
            processing_time = op['Processing Time']
            start_time = max(machine_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            final_schedule[job].append({
                'Operation': op['Operation'],
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[machine] = end_time
            job_completion_time[job] = end_time

    return final_schedule
