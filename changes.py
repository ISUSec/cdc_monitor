import time
import common
import datetime

if __name__ == '__main__':
	teams = [1]
	storage = {}

	for team in teams:
		storage[team] = common.getChecksPerTeam(team)

	while(True):
		for team in teams:
			checks = common.getChecksPerTeam(team)
			for index, check in enumerate(checks):
				if (storage[team][index][1] != check[1]):
					if check[1]:
						print("[{0}] Team {1} - {2} service has come online.".format(check[2].strftime("%H:%M"), team, check[0].strip()))
					else:
						print("[{0}] Team {1} - {2} service has gone down.".format(check[2].strftime("%H:%M"), team, check[0].strip()))						
			storage[team] = checks
		time.sleep(10)