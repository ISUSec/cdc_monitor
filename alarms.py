import time
import common
import datetime

if __name__ == '__main__':
	teams = [1]

	while(True):
		for team in teams:
			checks = common.getChecksPerTeam(team)
			for check in checks:
				if ((datetime.datetime.now() - check[2]).seconds > 30):
					print("[{0}] Team {1} - {2} check has died and needs to be restarted.".format(time.strftime("%H:%M"), team, check[0].strip()))
		time.sleep(10)

