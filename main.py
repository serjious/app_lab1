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
			"vehicle_id":	self.__vehicle_id,
			"make":			self.__make,
			"model":		self.__model,
			"year":			self.__year
		}

	def from_dict(self, data):
		self.__vehicle_id = data['vehicle_id'] 
		self.__make = data['make']
		self.__model = data['model'] 
		self.__year = data['year'] 

class Car(Vehicle):
	def __init__(self, vehicle_id: int, make: str,
				 model: str, year: int, doors: int):
		Vehicle.__init__(self, vehicle_id, make, model, year)
		self.__doors = doors

	def to_dict(self):
		data = Vehicle.to_dict(self)
		data['doors'] = self.__doors
		return data
	
	def from_dict(self, data):
		Vehicle.from_dict(self, data)
		self.__doors = data['doors']
		
class Truck(Vehicle):
	def __init__(self, vehicle_id: int, make: str,
				 model: str, year: int, capacity: float):
		Vehicle.__init__(self, vehicle_id, make, model, year)
		self.__capacity = capacity 

	def to_dict(self):
		data = Vehicle.to_dict(self)
		data['capacity'] = self.__capacity
		return data
	
	def from_dict(self, data):
		Vehicle.from_dict(self, data)
		self.__capacity= data['capacity']

class Motocycle(Vehicle):
	def __init__(self, vehicle_id: int, make: str,
				 model: str, year: int, type_moto: str):
		Vehicle.__init__(self, vehicle_id, make, model, year)
		self.__type_moto = type_moto

	def to_dict(self):
		data = Vehicle.to_dict(self)
		data['type_moto'] = self.__type_moto
		return data
	
	def from_dict(self, data):
		Vehicle.from_dict(self, data)
		self.__type_moto = data['type_moto']


def main():
	car = Car(1, "BMW", "X5", 2015, 4)
	truck = Truck(2,  "Scania", "hz", 2010, 200000)
	moto = Motocycle(3, "Honda", "hz2", 2020, 'sportbike')
	print(car.to_dict())
	print(truck.to_dict())
	print(moto.to_dict())



main()
