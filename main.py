import json

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

class File:
	def __init__(self, filename: str):
		try:
			self._file = open(filename, "w+")
		except OSError as e:
			print(e)
			exit(1)

	def file(self):
		return self._file
	
	def __del__(self):
		#self._file.close()
		pass

class JSON_File(File):
	def __init__(self, filename: str):
		if not (filename[-5:] == '.json'):
			filename += '.json'
		File.__init__(self, filename)
	
		
class XML_File(File):
	def __init__(self, filename: str):
		if not (filename[-4:] == '.xml'):
			filename += '.xml'
		File.__init__(self, filename)

class VehicleDatabase():
	def __init__(self, filename: str):
		self.__json_file = JSON_File(filename).file()
		self.__xml_file = XML_File(filename).file()
		self.__vehicles = {}
		self.__filename = filename
	
	def add_vehicle(self, vehicle: Vehicle):
		id_veh = vehicle.to_dict()['vehicle_id']
		if id_veh in self.__vehicles:
			raise InvalidVehicleDataError(
				f"Транспорт {id_veh} уже существует"
			)
		self.__vehicles[id_veh] = vehicle

	def get_vehicle(self, vehicle_id: int) -> Vehicle:
		if vehicle_id not in self.__vehicles:
			raise VehicleNotFoundError(vehicle_id)
		return self.__vehicles[vehicle_id]
	
	def update_vehicle(self, vehicle_id: int, vehicle: Vehicle):
		if vehicle_id not in self.__vehicles:
			raise VehicleNotFoundError(vehicle_id)
		self.__vehicles[vehicle_id] = vehicle

	def delete_vehicle(self, vehicle_id: int):
		if vehicle_id not in self.__vehicles:
			raise VehicleNotFoundError(vehicle_id)
		self.__vehicles.pop(vehicle_id)

	def to_json(self):
		self.__json_file.seek(0, 0)
		data = {vehicle_id: vehicle.to_dict()
					for vehicle_id, vehicle in self.__vehicles.items()}
		json.dump(data, self.__json_file, indent=4)
	
	def from_json(self):
		self.__json_file.seek(0, 0)
		data = json.load(self.__json_file)
		for veh_id, veh_data in data.items():
			if 'doors' in veh_data:
				vehicle = Car(veh_id, veh_data['make'], veh_data['model'],
							  veh_data['year'], veh_data['doors'])
			elif 'capacity' in veh_data:
				vehicle = Truck(veh_id, veh_data['make'], veh_data['model'],
							  veh_data['year'], veh_data['capacity'])
			elif 'type_moto' in veh_data:
				vehicle = Motocycle(veh_id, veh_data['make'],
									veh_data['model'], veh_data['year'],
									veh_data['type_moto'])
			else:
				continue
			self.add_vehicle(vehicle)
				

def main():
	db = VehicleDatabase("aboba")
	car = Car(1, "BMW", "X5", 2015, 4)
	car2 = Car(4, "AUDI", "fdg", 2002, 4)
	truck = Truck(2,  "Scania", "hz", 2010, 200000)
	moto = Motocycle(3, "Honda", "hz2", 2020, 'sportbike')
	
	db.add_vehicle(car)
	db.add_vehicle(truck)
	db.add_vehicle(moto)
	db.to_json()
	db.update_vehicle(1, car2)
	db.to_json()
	db.delete_vehicle(2)
	db.to_json()

main()

