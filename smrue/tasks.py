from celery import task

@task()
def add(x, y):
  print(x + y)
  return x + y