from distributor.tasks import spread_task

if __name__ == "__main__":
    print ("Starting distributor")
    try:
        spread_task.start_app()
    except Exception as e:
        print (f"Application error: {e}")
        exit(1)
