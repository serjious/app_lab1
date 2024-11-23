import json
import xml.etree.ElementTree as ET
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


class DriveLicense:
	def __init__(self, driver_license: str):
		if driver_license in "ABC":
			self._driver_license = driver_license
		else:
			self._driver_license = "None"


class Ticket:
	def __init__(self, ticket_id: int):
		if ticket_id < 0:
			raise ValueError('ticket_id должен быть больше 0')
		self._ticket_id = ticket_id
	
	def get_ticket_id(self):
		return self._ticket_id	


class Person:
	def __init__(self, name: str = "", age: int = 0):
		if not isinstance(name, str):
			raise TypeError('Некорректный тип name')
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


class Passenger(Person, Ticket):
	def __init__(self, name: str = "", age: int = 0, ticket_id: int = 0):
		Ticket.__init__(self, ticket_id)
		Person.__init__(self, name, age)
	
	def to_dict(self):
		data = Person.to_dict(self)
		data['ticket'] = self._ticket_id
		return data

	def from_dict(self, data):
		Person.from_dict(self, data)
		self._ticket_id = data['ticket']
	

class Driver(Person, DriveLicense):
	def __init__(self, name: str = "", age: int = 0, drive_license: str = ""):
		DriveLicense.__init__(self, drive_license)
		Person.__init__(self, name, age)
		if not isinstance(drive_license, str):
			raise TypeError('Некорректный тип drive_license}')

	def to_dict(self):
		data = Person.to_dict(self)
		data['drive_license'] = self._driver_license
		return data

	def from_dict(self, data):
		Person.from_dict(self, data)
		self._driver_license = data['drive_license']
			

class Engine:
	def __init__(self, power: int = 0):
		if power < 0:
			raise ValueError('Мощность двигателя должна быть больше 0 л.с.')
		self.__power = power

	def to_dict(self):
		return {'power': self.__power}


	def from_dict(self, data):
		self.__drive_license = data['power']


class Vehicle:
	def __init__(self, driver: Driver = Driver(), engine: int = 0, 
			vehicle_id: int = 0, make: str = "",
			model: str = None, year: int = 0):
		if not isinstance(driver, Driver):
			raise TypeError('Некорректный тип driver}')
		self.__driver = driver
		self.__engine = Engine(engine)
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
	def __init__(self, driver: Driver = Driver(), engine: int = 0,
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
	def __init__(self, driver: Driver = Driver(), engine: int = 0,
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
	def __init__(self, driver: Driver = Driver(), engine: int = 0,
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


class Bus(Vehicle):
	def __init__(self, driver: Driver = Driver(), engine: int = 0,
			vehicle_id: int = 0, make: str = "",
			model: str = "", year: int = 0, passangers: list = []):
		Vehicle.__init__(self, driver, engine,
			 vehicle_id, make, model, year)
		self.__passangers = passangers.copy()

	def to_dict(self):
		data = Vehicle.to_dict(self)
		z = {f"ID_pas_{i.get_ticket_id()}" : i.to_dict() for i in self.__passangers}
		data["passangers"] = z
		return data
	
	def from_dict(self, data):
		Vehicle.from_dict(self, data)
		self.__passangers = []
		for i, pas in data['passangers'].items():
			passangers = Passenger()
			passangers.from_dict(pas)
			self.__passangers.append(passangers)
		

class File:
	def __init__(self, filename: str, read: bool, binary: bool):
		if not read:
			if (os.path.isfile(filename)):
				os.remove(filename)	
			self._file = open(filename, "wb" if binary else "w")
		else:
			self._file = open(filename, "rb" if binary else "r")
			
	def file(self):
		return self._file
	
	def close(self):
		self._file.close()
		pass


class JSON_File(File):
	def __init__(self, filename: str, read: bool):
		if not filename:
			raise ValueError(f"Невозможно создать файл с именем {filename}")
		if not (filename[-5:] == '.json'):
			filename += '.json'
		File.__init__(self, filename, read, False)
	
		
class XML_File(File):
	def __init__(self, filename: str, read: bool):
		if not filename:
			raise ValueError(f"Невозможно создать файл с именем {filename}")
		if not (filename[-4:] == '.xml'):
			filename += '.xml'
		File.__init__(self, filename, read, True)


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
		file = JSON_File(self.__filename, read=False).file()
		data = {f"ID:{vehicle_id}": vehicle.to_dict()
			for vehicle_id, vehicle in self.__vehicles.items()}
		json.dump(data, file, indent=4)
		file.close()
	
	def from_json(self, obj: 'VehicleDatabase' = None):
		if obj == None:
			raise IODataBaseError("Нет объекта для записи")
		file = JSON_File(obj.__filename, read=True).file()
		data = json.load(file)
		for veh_id, veh_data in data.items():
			if 'doors' in veh_data:
				vehicle = Car()
			elif 'capacity' in veh_data:
				vehicle = Truck() 
			elif 'type_moto' in veh_data:
				vehicle = Motocycle() 
			elif 'passangers' in veh_data:
				vehicle = Bus()
			else:
				continue
			vehicle.from_dict(veh_data)
			self.add_vehicle(vehicle)
		file.close()
	
	def __dict_to_xml(self, tag, d):
		elem = ET.Element(str(tag))
		for key, val in d.items():
			child = ET.SubElement(elem, str(key))
			if isinstance(val, dict):
				child.append(self.__dict_to_xml(key, val))
			else:
				child.text = str(val) 
		return elem
		
	def to_xml(self):
		file = XML_File(self.__filename, read=False).file()
		data = {f"ID_vehicle_{vehicle_id}": vehicle.to_dict()
			for vehicle_id, vehicle in self.__vehicles.items()}
		xml_element = self.__dict_to_xml("root", data)
		tree = ET.ElementTree(xml_element)
		ET.indent(tree, "  ")
		tree.write(file, encoding="utf-8", xml_declaration=True)
		file.close()

	def from_xml(self, obj: 'VehicleDatabase' = None):
		if obj == None:
			raise IODataBaseError("Нет объекта для записи")
		
		file = XML_File(obj.__filename, read=True).file()
		tree = ET.parse(file)
		root = tree.getroot()
		file.close()

def main():
	db = VehicleDatabase("aboba")
	gg = VehicleDatabase("copy")
	pass1 = Passenger("Dima", 19, 1)
	pass2 = Passenger("Vova", 19, 2)
	pass3 = Passenger("Lesha", 19, 3)
	driver_car = Driver("Grisha", 19, "A")
	driver_car2 = Driver("Aziz", 18, "A")
	driver_truck = Driver("Misha", 19, "C")
	driver_moto = Driver("Nikita", 20, "B")
	driver_bus = Driver("Igor", 19, "С")
	car = Car(driver_car, 300, 1, "BMW", "X5", 2015, 4)
	car2 = Car(driver_car2, 150, 5, "AUDI", "fdg", 2002, 4)
	truck = Truck(driver_truck, 900, 2, "Scania", "hz", 2010, 200000)
	moto = Motocycle(driver_moto, 150, 3, "Honda", "hz2", 2020, 'sportbike')
	bus = Bus(driver_bus, 600, 4, "kamaz", "dw", 2017, [pass1, pass2, pass3])
	
	db.add_vehicle(car)
	db.add_vehicle(truck)
	db.add_vehicle(moto)
	db.add_vehicle(bus)
	#db.to_json()
	#db.update_vehicle(3, car2)
	#db.to_json()
	#db.delete_vehicle(3)
	db.to_json()
	db.to_xml()
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

