class VehicleError(Exception):
	pass

class VehicleNotFoundError(VehicleError):
	def __init__(self, vehicle_id):
		self.message=f"Транспортное средство с ID {vehicle_id} не найдено"
		super().__init__(self.message)

class InvalidVehicleDataError(VehicleError):
	def __init__(self, message):
		super().__init__(message)

class Vehicle:
	def __init__(self, vehicle_id: int, make: str, model: str, year: int):
		self.__vehicle_id = vehicle_id
		self.__make = make
		self.__model = model
		self.__year = year

	def to_dict(self):
		return {
			"vehicle_id": self.__vehicle_id,
			"make":		  self.__make,
			"model":	  self.__model,
			"year":		  self.__year
		}
	def from_dict(self, data):
		self.__vehicle_id = data['vehicle_id'] 
		self.__make = data['make']
		self.__model = data['model'] 
		self.__year = data['year'] 

def main():
	gfg = Vehicle(1, "BMW", "X5", 2015)
	d = gfg.to_dict()
	ddd = Vehicle(d['vehicle_id'], d['make'], d['model'], d['year'])
	print(ddd.to_dict())



main()
