"""
This module contains functions for running calculations using different packages.
It provides functions for running calculations with GAMESS US and NWChem.
The module also includes functions for handling job status, file upload, and cleanup.
"""
import time
import logging
import subprocess
import threading

from ivette.file_io_module import (
    convert_xyz_to_sdf,
    extract_geometries,
    generate_nwchem_input_from_sdf,
    get_step_data,
    get_total_dft_energy
)
from ivette.types import StoppableThread, ThermoData

from .IO_module import (
    get_cpu_core_count,
    setUp,
    cleanUp,
    check_gamess_installation,
    is_nwchem_installed,
    system_info,
    waiting_message,
    print_color
)

from .supabase_module import (
    downloadFile,
    get_dep_jobs,
    get_job_data,
    insert_step,
    update_job,
    uploadFile,
    insert_species,
    upsert_server
)

# Info disabling
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)
logging.getLogger("gql").setLevel(logging.CRITICAL)

# Create a flag to signal when the job is done
job_done = False
job_failed = False
operation = None
should_exit = False
step_thread = StoppableThread()


def run_rungms(job_id, nproc):  # deprecated
    """
    Run the 'rungms' command with the given id and number of processors.

    Args:
        id (str): The id of the command.
        nproc (int): The number of processors to use.

    Raises:
        subprocess.CalledProcessError: If the 'rungms' command returns a non-zero exit code.

    Returns:
        None
    """

    print("GAMESS US is deprecated")
    global job_done
    global job_failed

    command = ["rungms tmp/" + job_id + " 00 " +
               str(nproc)]  # The last one is ncores

    with open(f"tmp/{job_id}.out", "w", encoding='utf-8') as output_file:
        try:

            # Run the 'rungms' command and wait for it to complete
            subprocess.run(
                command,
                stdout=output_file,
                stderr=subprocess.STDOUT,
                shell=True,
                check=True,  # This will raise an error if the command returns a non-zero exit code
            )

            uploadFile(f"{job_id}.out", job_id, bucketName="Outputs", localDir="tmp/")
            update_job(job_id, nproc=0)
            job_done = True

        except subprocess.CalledProcessError as e:
            if not e.returncode == -2:

                update_job(job_id, "failed", nproc=0)
                uploadFile(f"{job_id}.out", job_id, bucketName='Outputs', localDir="tmp/")

            cleanUp(job_id)
            print(f"\n Job failed with exit code {e.returncode}.")
            job_done = True
            job_failed = True


def run_command(command, job_id):
    with open(f"tmp/{job_id}.out", "w", encoding='utf-8') as output_file:
        subprocess.run(
            command,
            stdout=output_file,
            stderr=subprocess.STDOUT,
            shell=True,
            check=True,  # This will raise an error if the command returns a non-zero exit code
        )


def handle_optimize_operation(job_id, nproc):
    # Create a new species for the optimized geometry
    species_id = insert_species(f'{job_id} opt')

    # Extract the optimized geometry from the output file
    extract_geometries(
        f"tmp/{job_id}.out", f"tmp/{species_id}.xyz")
    convert_xyz_to_sdf(
        f"tmp/{species_id}.xyz", f"tmp/{species_id}.sdf")

    # Generate input file
    jobs = get_dep_jobs(job_id)

    for job in jobs:
        generate_nwchem_input_from_sdf(
            f"tmp/{species_id}.sdf",
            job.get('basisSet'),
            job.get('charge'),
            job.get('id'),
            functional=job.get('functional'),
            multiplicity=job.get('multiplicity'),
            operation="energy" if (job.get('operation').upper() ==
                                   'COSMO') else job.get('operation'),
            cosmo=True if (job.get('operation').upper() == 'COSMO') else False
        )

        uploadFile(f"tmp/{species_id}.nw",
                   job.get('id'), bucketName='Inputs')

    # Upload the optimized geometry
    uploadFile(f"{species_id}.sdf", species_id,
               bucketName='Species', localDir='tmp/')
    uploadFile(f"{job_id}.out", job_id, bucketName="Outputs", localDir="tmp/")

    # Set step data
    step_data = get_step_data(f"tmp/{job_id}.out")

    # Upload data from the current job
    thermo_data = ThermoData(
        energy=step_data.energy if step_data is not None else None)
    update_job(job_id, "done", nproc=0, species_id=species_id,
               thermo_data=thermo_data)


def handle_other_operations(job_id, nproc):
    # Create a new species for the optimized geometry
    jobs = get_dep_jobs(job_id)
    current_job = get_job_data(job_id)

    # Extract the optimized geometry from the output file
    extract_geometries(
        f"tmp/{job_id}.out", f"tmp/{current_job.get('inputSpeciesId')}.xyz")
    convert_xyz_to_sdf(
        f"tmp/{current_job.get('inputSpeciesId')}.xyz", f"tmp/{current_job.get('inputSpeciesId')}.sdf")

    # Generate input file
    for job in jobs:

        generate_nwchem_input_from_sdf(
            f"tmp/{current_job.get('inputSpeciesId')}.sdf",
            job.get('basisSet'),
            job.get('charge'),
            job.get('id'),
            functional=job.get('functional'),
            multiplicity=job.get('multiplicity'),
            operation="energy" if (job.get('operation').upper() ==
                                   'COSMO') else job.get('operation'),
            cosmo=True if (job.get('operation').upper()
                           == 'COSMO') else False
        )

        uploadFile(f"tmp/{current_job.get('inputSpeciesId')}.nw",
                   job.get('id'), bucketName='Inputs')

    # Upload the output file
    uploadFile(f"{job_id}.out", job_id, bucketName="Outputs", localDir="tmp/")

    # Upload data from the current job
    if current_job.get('operation').upper() in ['ENERGY', 'COSMO', 'FREQ']:

        thermo_data = ThermoData(
            energy=get_total_dft_energy(f"tmp/{job_id}.out"))
        update_job(job_id, "done", nproc=0, thermo_data=thermo_data)


def run_nwchem(job_id, nproc):
    """
    Run the calculation
    """

    global job_done
    global job_failed

    if nproc:
        command = [
            f"mpirun -np {nproc} --use-hwthread-cpus $NWCHEM_TOP/bin/$NWCHEM_TARGET/nwchem tmp/{job_id}"]
    else:
        command = [
            f"mpirun -map-by core --use-hwthread-cpus $NWCHEM_TOP/bin/$NWCHEM_TARGET/nwchem tmp/{job_id}"]

    try:
        run_command(command, job_id)

        if operation and operation.upper() == "OPTIMIZE":
            handle_optimize_operation(job_id, nproc)
        else:
            handle_other_operations(job_id, nproc)

        job_done = True

    except subprocess.CalledProcessError as e:
        if not e.returncode == -2:
            update_job(job_id, "failed", nproc=0)
            uploadFile(f"{job_id}.out", job_id,
                       bucketName='Outputs', localDir="tmp/")
        print(f"\n\n Job failed with exit code {e.returncode}.")
        job_done = True
        job_failed = True
        raise SystemExit from e


def run_job(nproc=None):
    """
    Run the job based on the specified package and number of processors.

    Args:
        nproc (int, optional): Number of processors to use. Defaults to None.

    Raises:
        SystemExit: If the job is interrupted by the user.

    Returns:
        None
    """
    global job_done
    global operation
    global job_failed
    global should_exit
    print("Press Ctrl + C at any time to exit.")

    # Loop over to run the queue
    while True:

        JOB_ID, package, operation = setUp()
        downloadFile(JOB_ID, dir='tmp/', bucket_name="Inputs")

        if package in ["GAMESS US", "NWChem"] and (check_gamess_installation if package == "GAMESS US" else is_nwchem_installed):
            if not nproc:
                nproc = get_cpu_core_count()

            # Create a thread to run the command
            run_thread = threading.Thread(
                target=run_rungms if package == "GAMESS US" else run_nwchem, args=(JOB_ID, nproc))

            # Create a thread to run the function
            step_thread = StoppableThread(
                target=periodical_updates, args=(f'tmp/{JOB_ID}.out', JOB_ID))
            step_thread.daemon = True
            
            try:
                update_job(JOB_ID, "in progress",
                           nproc if nproc else get_cpu_core_count())  # type: ignore

                print(f"Job Id: {JOB_ID}")
                run_thread.start()  # Start the command thread
                step_thread.start()

                while not job_done:
                    waiting_message(package)
                    if should_exit:
                        print("Turning off requested, waiting for job to finish...",
                              flush=True)
                        raise Exception("Turning off requested")

                run_thread.join()  # Wait for the command thread to finish
                step_thread.stop()
                cleanUp(JOB_ID)

                if not job_failed:
                    print_color("✓ Job completed successfully.", "32")

                job_done = False
                job_failed = False

            except KeyboardInterrupt as exc:
                update_job(JOB_ID, "interrupted", nproc=0)
                upsert_server(system_info(), "offline")
                
                run_thread.join()  # Wait for the command thread to finish
                step_thread.stop()
                cleanUp(JOB_ID)
                print(" Job interrupted.       ")
                raise SystemExit from exc
            
            except Exception as exc:
                run_thread.join()  # Wait for the command thread to finish
                step_thread.stop()
                upsert_server(system_info(), "offline")
                cleanUp(JOB_ID)
                print_color("✓ Job completed successfully.", "32")
                raise SystemExit from exc

        else:
            print(f"No package called: {package}. Contact support.")
            raise SystemExit


def periodical_updates(file, JOB_ID):
    global operation
    global should_exit
    last_step = None
    last_index = -1

    while True:
        # Update server status
        if upsert_server(system_info(), "online") == "turn off":
            should_exit = True

        if step_thread.stopped():
            break

        # Get step data
        try:
            step_data = get_step_data(file, last_index + 1)
            while step_data is not None:
                # If operation is optimize and it's a new step, insert step
                if operation == 'optimize' and step_data != last_step:
                    insert_step(JOB_ID, step_data)
                    last_step = step_data
                last_index += 1
                step_data = get_step_data(file, last_index + 1)
        except FileNotFoundError:
            time.sleep(5)
            continue

        # Sleep for a period of time (e.g., 5 seconds)
        time.sleep(5)
