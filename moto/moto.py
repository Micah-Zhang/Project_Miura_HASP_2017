def main(run_exp, moto_cmd):
	while(True):
		if(run_exp.is_set()==True):
			print("run_exp is set verified")
			cycle = 1
			while cycle<3:
				fmoto.minimum_success(moto_cmd)
				fmoto.receive_command(moto_cmd) #why are there so many "recieve_commands"? Do we really need all of them?
				cycle+=1
			while cycle>2:
				fmoto.full_extension(moto_cmd)
				fmoto.receive_command(moto_cmd)
				cycle+=1

if __name__ == "__main__":
	import fmoto
	from fmoto import *
	main()
else:
	import moto.fmoto as fmoto
	from moto.fmoto import *

