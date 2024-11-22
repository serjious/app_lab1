import json
import os

class TusovaError(Exception):
	pass


class VehicleNotFoundError(TusovaError):
	def __init__(self, vehicle_id):
		self.message=f"Транспортное средство с ID {vehicle_id} не найдено"
		super().__init__(self.message)


class InvalidVehicleDataError(TusovaError):
	def __init__(self, message):
		super().__init__(message)


class IODataBaseError(TusovaError):
	def __init__(self, message):
		super().__init__(message)


class Person:
	def __init__(self, name: str = "", age: int = 0):
		if not isinstance(name, str):
			raise TypeError(f'Некорректный тип {name.type()}')
		if not isinstance(age, int) or age < 0:
			raise ValueError('Возраст должен быть больше 0')
		self.__name = name
		self.__age = age

	def to_dict(self):
		return {
			"name": self.__name,
			"age": self.__age,
		}

	def from_dict(self, data):
		self.__name = data['name']
		self.__age = data['age']

	
class Driver(Person):
	def __init__(self, name: str = "", age: int = 0, drive_license: str = ""):
		Person.__init__(self, name, age)
		if not isinstance(drive_license, str) :
			raise TypeError(f'Некорректный тип {drive_license.type()}')
		self.__drive_license = drive_license

	def to_dict(self):
		data = Person.to_dict(self)
		data['drive_license'] = self.__drive_license
		return data

	def from_dict(self, data):
		Person.from_dict(self, data)
		self.__drive_license = data['drive_license']
			

class Engine:
	def __init__(self, power: int = 0):
		if not isinstance(power, int) or power < 0:
			raise ValueError('Мощность двигателя должна быть больше 0 л.с.')
		self.__power = power

	def to_dict(self):
		return {'power': self.__power}


	def from_dict(self, data):
		self.__drive_license = data['power']


class Vehicle:
	def __init__(self, driver: Driver = Driver(), engine: Engine = Engine(), 
				 vehicle_id: int = 0, make: str = "", 
				 model: str = None, year: int = 0):
		self.__driver = driver
		self.__engine = engine
		self.__vehicle_id = vehicle_id
		self.__make = make
		self.__model = model
		self.__year = year

	def to_dict(self):
		data = {
			"driver":		self.__driver.to_dict(),
			"engine":		self.__engine.to_dict(),
			"vehicle_id":		self.__vehicle_id,
			"make":			self.__make,
			"model":		self.__model,
			"year":			self.__year
		}
		return data 

	def from_dict(self, data):
		self.__driver.from_dict(data['driver'])
		self.__engine.from_dict(data['engine'])
		self.__vehicle_id = data['vehicle_id'] 
		self.__make = data['make']
		self.__model = data['model'] 
		self.__year = data['year'] 


class Car(Vehicle):
	def __init__(self, driver: Driver = Driver(), engine: Engine = Engine(),
				 vehicle_id: int = 0, make: str = "",
				 model: str = "", year: int = 0, doors: int = 0):
		Vehicle.__init__(self, driver, engine,
				 vehicle_id, make, model, year)
		self.__doors = doors

	def to_dict(self):
		data = Vehicle.to_dict(self)
		data['doors'] = self.__doors
		return data
	
	def from_dict(self, data):
		Vehicle.from_dict(self, data)
		self.__doors = data['doors']
		

class Truck(Vehicle):
	def __init__(self, driver: Driver = Driver(), engine: Engine = Engine(),
				 vehicle_id: int = 0, make: str = "",
				 model: str = "", year: int = 0, capacity: float = 0):
		Vehicle.__init__(self, driver, engine,
				 vehicle_id, make, model, year)
		self.__capacity = capacity 

	def to_dict(self):
		data = Vehicle.to_dict(self)
		data['capacity'] = self.__capacity
		return data
	
	def from_dict(self, data):
		Vehicle.from_dict(self, data)
		self.__capacity = data['capacity']


class Motocycle(Vehicle):
	def __init__(self, driver: Driver = None, engine: Engine = None,
				 vehicle_id: int = 0, make: str = "",
				 model: str = "", year: int = 0, type_moto: str = ""):
		Vehicle.__init__(self, driver, engine,
				 vehicle_id, make, model, year)
		self.__type_moto = type_moto

	def to_dict(self):
		data = Vehicle.to_dict(self)
		data['type_moto'] = self.__type_moto
		return data
	
	def from_dict(self, data):
		Vehicle.from_dict(self, data)
		self.__type_moto = data['type_moto']


class File:
	def __init__(self, filename: str, read: bool):
		if not read:
			if (os.path.isfile(filename)):
				os.remove(filename)	
			self._file = open(filename, "w")
		else:
			self._file = open(filename, "r")
			
	def file(self):
		return self._file
	
	def close(self):
		self._file.close()
		pass


class JSON_File(File):
	def __init__(self, filename: str, read: bool):
		if not (filename[-5:] == '.json'):
			filename += '.json'
		File.__init__(self, filename, read)
	
		
class XML_File(File):
	def __init__(self, filename: str, read: bool):
		if not (filename[-4:] == '.xml'):
			filename += '.xml'
		File.__init__(self, filename, read)


class VehicleDatabase():
	def __init__(self, filename: str):
		self.__filename = filename
		self.__vehicles = {}
	
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
		self.__json_file = JSON_File(self.__filename, read=False).file()
		data = {vehicle_id: vehicle.to_dict()
			for vehicle_id, vehicle in self.__vehicles.items()}
		json.dump(data, self.__json_file, indent=4)
		self.__json_file.close()
	
	def from_json(self, obj: 'VehicleDatabase'):
		if obj == None:
			raise IODataBaseError("Нет объекта для записи")
		obj.__json_file = JSON_File(obj.__filename, read=True).file()
		data = json.load(obj.__json_file)
		for veh_id, veh_data in data.items():
			if 'doors' in veh_data:
				vehicle = Car()
			elif 'capacity' in veh_data:
				vehicle = Truck() 
			elif 'type_moto' in veh_data:
				vehicle = Motocycle() 
			else:
				continue
			vehicle.from_dict(veh_data)
			self.add_vehicle(vehicle)
		obj.__json_file.close()
				

def main():
	db = VehicleDatabase("aboba")
	gg = VehicleDatabase("copy")
	en_car = Engine(300)
	en_moto = Engine(350)
	en_truck = Engine(900)
	driver_car = Driver("Grisha", 19, "A")
	driver_car2 = Driver("Aziz", 18, "B")
	driver_truck = Driver("Misha", 19, "C")
	driver_moto = Driver("Nikita", 20, "D")
	car = Car(driver_car, en_car, 1, "BMW", "X5", 2015, 4)
	car2 = Car(driver_car2, en_car, 4, "AUDI", "fdg", 2002, 4)
	truck = Truck(driver_truck, en_truck, 2, "Scania", "hz", 2010, 200000)
	moto = Motocycle(driver_moto, en_moto, 3, "Honda", "hz2", 2020, 'sportbike')
	
	db.add_vehicle(car)
	db.add_vehicle(truck)
	db.add_vehicle(moto)
	db.to_json()
	db.update_vehicle(3, car2)
	db.to_json()
	db.delete_vehicle(3)
	db.to_json()
	gg.from_json(db)
	gg.to_json()

main()
'''
try:
	main()
except Exception as e:
	print(e)
	exit(1)
'''

