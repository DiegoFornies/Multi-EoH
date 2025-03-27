
def heuristic(input_data):
    """A heuristic for FJSSP using Shortest Processing Time first."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            op_num = op_idx + 1
            machines_options = []
            for m_idx, machine in enumerate(operation[0]):
                machines_options.append((operation[1][m_idx],machine))
            machines_options.sort(key=lambda x: x[0])

            best_machine = None
            best_processing_time = None
            best_start_time = None

            for processing_time, machine in machines_options:
                start_time = max(machine_available_time[machine], job_completion_time[job])

                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time
                break

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time

    return schedule
