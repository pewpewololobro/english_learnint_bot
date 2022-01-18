from model import User
from server import get_test
import schedule, time

def job():
	users = User.select()
	for user in users:
		get_test(None, user)

if __name__ == '__main__':
	schedule.every(10).seconds.do(job)
	while True:
		schedule.run.pedding()
		time.sleep(1)