import random

class Spaceteam(object):
	CalciumRazor = 0
	LorentzWhittler = 0
	KilobyPass = 0
	IodineShower = 0
	ContractingPropeller = 0
	Quasipaddle = 0
	Holospindle = 0
	ArcballPendulum = 0
	PressurizedVarnish = 0
	Orbring = 0
	FluxloosenerOptimizer = 0
	PsilocybinCapacitor = 0
	ProtolubeOptimizer = 0
	SaltyCanister = 0
	AltitudeOperator = 0

	gameOver = 0
	life = 5
	level = 1

	def getCommand(self):
		done = 0
		print("\tGetting the Command")
		button = random.randint(1,14)
		if(button == 1):
			if self.CalciumRazor == 0: #check the state of the Calcium Razor if Engaged of not
				action = input("Toggle On Calcium Razor") 
				if(action == 1):
					self.CalciumRazor == 1
					#killtime get command
			else:  
				action = input("Toggle On Calcium Razor")
				if(action == 0):
					self.CalciumRazor == 0
					#killtime
		elif(button == 2):
			randomOption = random.randint(1,3)
			if( randomOption == 1):
				action = input("Set Lorentz Whittler to Min")
				#killtime
			elif(randomOption == 3):
				action = input("Set Lorentz Whittler to Max")
				#killtime
			else:
				randomOption = random.randint(2,4) #not min not max
				action = int(input("Set Lorentz Whittler to {}".format(randomOption)))
				#killtime
		elif(button == 3):
			if self.KilobyPass == 0: #check the state of Kilo By Pass if Engaged of not
				action = input("Engage Kilo by Pass") 
				#kill time
			else: 
				action = input("Disengage Kilo by Pass")
				#kill time
		elif(button == 4):
			if self.IodineShower == 0: #check the state of Kilo By Pass if Engaged of not
				action = input("Infuse Iodine Shower") 
				#kill time
			else:  
				action = input("Defuse Iodine Shower")
				#kill time
		elif(button == 5):
			randomOption = random.randint(1,3)
			if(randomOption == 1):
				action = input("Release Contracting Propeller")
			elif (randomOption == 2):
				action = input("Kick Contracting Propeller")
			else:
				action = input("Acquire Contracting Propeller")
		elif(button == 6):
			randomOption = random.randint(1,3)
			if( randomOption == 1):
				action = input("Engage Quasipaddle to Min")
				#killtime
			elif(randomOption == 3):
				action = input("Engage Quasipaddle to Max")
				#killtime
			else:
				randomOption = random.randint(2,4) #not min not max
				action = int(input("Engage Quasipaddle to {}".format(randomOption)))
		elif(button == 7):
			randomOption = random.randint(0,2)
			action = int(input("Turn Holospindle to {}".format(randomOption)))
		elif(button == 8):
			if self.ArcballPendulum == 0: #check the state of the Calcium Razor if Engaged of not
				action = input("Switch On Arcball Pendulum") 
				#kill time
			else:  
				action = input("Switch Off Arcball Pendulum")
				#kill time
		elif(button == 9):
			randomOption = random.randint(0,3)
			action = int(input("Lock Pressurized Varnish to {}".format(randomOption)))
		elif(button == 10):
			if self.Orbring == 0: #check the state of the Calcium Razor if Engaged of not
				action = input("Power Up Orbring") 
				#kill time
			else:  
				action = input("Power Off Orbring")
		elif(button == 11):
			action = input("Flush Fluxloosener Optimizer")
		elif(button == 12):
			if self.ProtolubeOptimizer == 0: #check the state of the Calcium Razor if Engaged of not
				action = input("Fragment Protolube Optimizer") 
				#kill time
			else:  
				action = input("Defragment Protolube Optimizer")
		elif(button == 13):
			randomOption = random.randint(5,10) * 10
			action = int(input("Set Psilocybin Capacitor Temperature to {}".format(randomOption)))
		elif(button == 14):
			if self.SaltyCanister == 0: #check the state of the Calcium Razor if Engaged of not
				action = input("Open Salty Canister") 
				#kill time
			else:  
				action = input("Close Salty Canister")
		elif(button == 15):
			if self.AltitudeOperator == 0: #check the state of the Calcium Razor if Engaged of not
				action = input("Kick Altitude Operator") 
				#kill time
			else:  
				action = input("Approach Altitude Operator")


	def main(self):
		while self.gameOver < 15 and self.life > 0:
			self.getCommand()
			self.gameOver = self.gameOver + 1


x = Spaceteam()
x.main()