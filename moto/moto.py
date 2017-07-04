def main():
	cycle = 1
	while cycle<3:
		fmoto.minimum_success()
		fmoto.receive_command() #why are there so many "recieve_commands"? Do we really need all of them?
		cycle+=1
	while cycle>2:
		fmoto.full_extension()
		fmoto.receive_command()
		cycle+=1

if __name__ == "__main__":
	import fmoto
	from fmoto import *
	main()
else:
	import moto.fmoto as fmoto
	from moto.fmoto import *

