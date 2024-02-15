from modules import launch_utils

args = launch_utils.args
python = launch_utils.python
git = launch_utils.git
index_url = launch_utils.index_url

run = launch_utils.run
is_installed = launch_utils.is_installed
run_pip = launch_utils.run_pip
check_run_python = launch_utils.check_run_python
prepare_environment = launch_utils.prepare_environment
start = launch_utils.start


def main():
    if args.dump_sysinfo:
        filename = launch_utils.dump_sysinfo()

        print(f"Sysinfo saved as {filename}. Exiting...")
        exit(0)

    launch_utils.startup_timer.record("initial startup")

    with launch_utils.startup_timer.subcategory("prepare environment"):
        if not args.skip_prepare_environment:
            prepare_environment()

    start()


if __name__ == "__main__":
    main()
