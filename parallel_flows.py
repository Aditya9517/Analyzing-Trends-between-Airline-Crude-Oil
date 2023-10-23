from prefect import task, flow #-Line 1
from prefect_dask.task_runners import DaskTaskRunner #-Line 2

#print square of a number
@task #-Line 3
def print_squares(element):#-Line4
    square = element ** 2
    print(square)

#The flow that is going to call the tasks
#This function will be the entry point for our script
@flow(task_runner=DaskTaskRunner())#-Line 5
def my_flow(elements):#-Line 6
    for element in elements:
        print_squares.submit(element)#-Line 7

if __name__ == "__main__":
    elements = [1, 2, 3, 4, 5]
    my_flow(elements)
