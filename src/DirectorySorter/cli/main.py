from organizer import app
if __name__ == "__main__":
    # Ask the user for the directory that should be organized.
    directory_path = input("Enter the directory path to organize: ")

    # Create the application and start the organization process.
    prog = app.App(directory_path)
    prog.run()
