#!/usr/bin/env python3
import os
import subprocess
import sys
import time
import json

# Code by Tunjay Akbarli. 
# Creation Date: September 16th, 2024.

def load_project_code():
    """Loads the project.code file as JSON-like data if it exists."""
    if not os.path.exists("project.code"):
        return None  # No project.code file found
    
    with open("project.code", "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Error: project.code is not valid JSON.")
            sys.exit(1)

def install_dependencies(dependencies, verbose=False):
    """Installs dependencies using pip or another package manager."""
    if dependencies:
        for dep in dependencies:
            if verbose:
                print(f"Installing dependency: {dep}")
            subprocess.run([sys.executable, "-m", "pip", "install", dep])

def run_main_script(main_file):
    """Runs the main script defined in project.code or passed explicitly."""
    current_dir = os.getcwd()
    code_file_path = os.path.join(current_dir, main_file)
    py_file_path = code_file_path[:-5] + ".py"

    if not os.path.exists(code_file_path):
        print(f"Error: Main file {main_file} not found.")
        return

    # Rename .code file to .py temporarily (hidden from user)
    os.rename(code_file_path, py_file_path)

    try:
        # Run the file using Pyston interpreter
        result = subprocess.run(["pyston", py_file_path], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
    finally:
        # Rename back to .code (hidden from user)
        os.rename(py_file_path, code_file_path)

def find_code_files():
    """Finds all .code files in the current directory."""
    current_dir = os.getcwd()
    return [f for f in os.listdir(current_dir) if f.endswith(".code")]

def watch_file(file_name):
    """Watches a file and reruns it when it changes."""
    if not os.path.isfile(file_name):
        print(f"Error: {file_name} does not exist.")
        return
    
    last_modified_time = os.path.getmtime(file_name)
    
    print(f"Watching {file_name} for changes. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
            current_modified_time = os.path.getmtime(file_name)
            if current_modified_time != last_modified_time:
                print(f"Detected change in {file_name}. Rerunning...")
                run_main_script(file_name)
                last_modified_time = current_modified_time
    except KeyboardInterrupt:
        print("\nStopped watching the file.")

def clean_project():
    """Cleans up build artifacts or temporary files."""
    if os.path.exists("__pycache__"):
        subprocess.run(["rm", "-rf", "__pycache__"])
    print("Cleaned project.")

def build_project(build_commands, verbose=False):
    """Executes build commands from project.code if available."""
    if not build_commands:
        print("No build commands found.")
        return

    for command in build_commands:
        if verbose:
            print(f"Running build command: {command}")
        subprocess.run(command, shell=True)

def restore_project():
    """Restores dependencies for the project."""
    print("Restoring dependencies...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"])

def run_tests(test_commands):
    """Runs tests defined in the project."""
    if not test_commands:
        print("No test commands found.")
        return
    
    for command in test_commands:
        print(f"Running test command: {command}")
        subprocess.run(command, shell=True)

def add_package(package_name):
    """Adds a package to the project."""
    print(f"Adding package: {package_name}")
    subprocess.run([sys.executable, "-m", "pip", "install", package_name])

def handle_package_command(args):
    """Handles 'package' command aliases."""
    if not args:
        print("Error: No package action specified.")
        return
    
    action = args[0]
    package_args = args[1:]

    if action == "install":
        if not package_args:
            print("Error: Package name must be provided.")
            return
        subprocess.run([sys.executable, "-m", "pip", "install"] + package_args)
    
    elif action == "uninstall":
        if not package_args:
            print("Error: Package name must be provided.")
            return
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y"] + package_args)
    
    elif action == "list":
        subprocess.run([sys.executable, "-m", "pip", "list"])
    
    elif action == "freeze":
        subprocess.run([sys.executable, "-m", "pip", "freeze"])
    
    else:
        print(f"Error: Unknown package action '{action}'")

def print_help():
    """Prints help/usage information."""
    help_text = """
Usage: nextcode <command> [options]

Commands:
  run           Run the main .code file defined in project.code or the first available .code file
  build         Build the project using commands defined in project.code (if available)
  install       Install dependencies listed in project.code (if available)
  clean         Clean up temporary files and build artifacts
  watch         Watch the main .code file for changes and re-run on modification
  restore       Restore project dependencies
  test          Run tests using commands defined in project.code (if available)
  add           Add a package to the project
  package       Alias for package manager commands (install, uninstall, list, freeze)
  -h, --help    Show this help message and exit

Additional Commands:
  dev-certs     Create and manage development certificates.
  user-jwts     Manage JSON Web Tokens in development.
  user-secrets  Manage development user secrets.
"""
    print(help_text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: nextcode <command> [options]")
        sys.exit(1)

    # Load project.code if available
    project = load_project_code()

    # Set defaults if project.code is missing
    main_file = "main.code" if project is None else project.get("main", "main.code")
    dependencies = [] if project is None else project.get("dependencies", [])
    build_commands = [] if project is None else project.get("build", [])
    test_commands = [] if project is None else project.get("test", [])
    
    # Command and options
    command = sys.argv[1]
    additional_args = sys.argv[2:]

    if command == "run":
        if not project:
            # Find .code file if no project.code and no main file specified
            code_files = find_code_files()
            if len(code_files) == 0:
                print("Error: No .code file found in the current directory.")
                sys.exit(1)
            elif len(code_files) > 1:
                print("Error: Multiple .code files found. Specify the main file in project.code or use one manually.")
                sys.exit(1)
            else:
                main_file = code_files[0]
        
        install_dependencies(dependencies)
        run_main_script(main_file)
    
    elif command == "build":
        if not project:
            print("No project.code file found. No build commands available.")
        else:
            build_project(build_commands)
    
    elif command == "install":
        install_dependencies(dependencies)
    
    elif command == "clean":
        clean_project()
    
    elif command == "watch":
        if not project:
            # Default to first .code file if no project.code
            code_files = find_code_files()
            if len(code_files) == 0:
                print("Error: No .code file found in the current directory.")
                sys.exit(1)
            main_file = code_files[0]
        
        watch_file(main_file)
    
    elif command == "restore":
        restore_project()
    
    elif command == "test":
        run_tests(test_commands)
    
    elif command == "add":
        if not additional_args:
            print("Error: Package name must be provided.")
            sys.exit(1)
        add_package(additional_args[0])
    
    elif command == "package":
        handle_package_command(additional_args)
    
    elif command in ("-h", "--help"):
        print_help()
    
    else:
        print(f"Error: Unknown command '{command}'")
        print_help()
