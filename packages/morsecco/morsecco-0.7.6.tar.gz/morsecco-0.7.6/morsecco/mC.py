# morseccoClasses (mC) contains the classes used by morsecco, some utilities and the globals

import sys, re, os, random, time, datetime
import urllib.request
from collections import UserDict
from alphabet import morsecodes

acceptSlash = True
endOfToken = ['', ' ', '\n', '\r', '\t', '\d', chr(9723)]
dots = '.·∙'
strokes = '-–/'
timeFormat = '-.-- -- -.. .... .. ...'

class Cell:
	def __init__(self, content = ''):
		self.content = content
	def copy(self):
		return Cell(self.content)
	def getToken(self, clean=False):
		if len(self.content) == 0:
			error("Requesting token from empty cell.")
			return ''
		elif self.content == ' ': # just one empty token
			self.content=''
			return ''
		split=self.content.split(' ',1)
		if len(split) < 2:
			self.content=''
		elif split[1]:
			self.content = split[1]
		else:
			self.content = ' ' # preserve trailing empty token
		if clean:
			return split[0]
		elif acceptSlash:
			return re.sub('[^ .-]', '', split[0].replace('/','-').replace('∙','.'))
		else:
			return re.sub('[^ .-]', '', split[0])
	def getInt(self):
		split=self.content.split(' ',1)
		if len(split) == 1:
			self.content = ''
		elif len(split) == 2:
			self.content = split[1]
		if split[0] == '':
			error("Requesting number from an empty cell.")
			return 0
		return code2int(split[0])
	def getFloat(self):
		split=self.content.split(' ',1)
		if len(split) == 1:
			self.content = ''
		elif len(split) == 2:
			self.content = split[1]
		if split[0] == '':
			error("Requesting number from an empty cell.")
			return 0
		return code2float(split[0])
	def len(self):
		return len(self.content)
	def append(self, other):
		return Cell(self.content + other.content)
	def add(self, other):
		sum = ''
		while self.len() > 0 and other.len() > 0:
			sum = sum + float2code(code2float(self.getToken()) + code2float(other.getToken())) + ' '
		sum = sum + self.content + other.content
		return Cell(sum.strip())
	def binary(self, other, operation):
		result = ''
		if operation == '-..' and self.content != other.content:
			for i in range(max(len(self.content), len(other.content))):
				if i < min(len(self.content), len(other.content)):
					if self.content[i] == other.content[i]:
						result += '.'
					else:
						result += '-'
				else:
					result += '-'
		elif operation in ['.-', '---', '-..-']:
			while self.len() > 0 and other.len() > 0:
				if operation == '.-': # and
					result = result + int2code(abs(code2int(self.getToken())) & abs(code2int(other.getToken()))) + ' '
				elif operation == '---': # or
					result = result + int2code(abs(code2int(self.getToken())) | abs(code2int(other.getToken()))) + ' '
				elif operation == '-..-': # xor
					result = result + int2code(abs(code2int(self.getToken())) ^ abs(code2int(other.getToken()))) + ' '
			result = result + self.content + other.content
		return Cell(result.strip())
	def getExecutionPointer(self):
		generation = 0
		while len(self.content) > 0 and self.content[0] == ' ':
			generation += 1
			self.content = self.content[1:]
		if not ' ' in self.content: # Doesn't look like an address
			error(f"illegal address »{self.content}«")
		else:
			pos = self.getInt()
			id = self.content
			if not storage.exists(id):
				error(f"addressing unexistent command {id}")
			if pos < 0:
				error(f"addressing negative command position {pos}")
			return ExecutionPointer(id = id, position = pos, generation = generation)
		return ep.copy()
	def toTime(self):
		return Time(self.content)

class ExecutionPointer:
	def __init__(self, id, position = 0, generation = 0):
		self.id = id
		self.position = position
		self.generation = generation
	def isValid(self):
		target = self.getCell()
		if not target:
			return False
		if self.position >= 0 and self.position <= target.len():
			return True
		else:
			return False
	def copy(self):
		return ExecutionPointer(self.id, self.position, self.generation)
	def getCell(self):
		generation = self.generation
		targetStorage = storage
		while generation > 0:
			targetStorage = targetStorage.children['']
			if targetStorage:
				generation -= 1
			else:
				return False
		if targetStorage.exists(self.id):
			return targetStorage.cells[self.id]
		else:
			return False
	def getToken(self):
		token=''
		source = self.getCell().content
		if self.position >= len(source):
			return chr(0)
		while self.position < len(source):
			char = source[self.position]
			self.position = self.position + 1
			if char in dots: # '.·∙':
				token += '.'
			elif char in strokes: # '-–/':
				token += '-'
			elif char in endOfToken: #[' ', '\n', '\r', '\t', chr(9723)]:
				break
		return token
	def back(self): # move position one token backwards
		if self.position == 0:
			error(f"Already at the start of the command sequence.")
		else:
			source = self.getCell().content
			position = self.position
			while position := position - 1:
				if source[position - 1] in [' ', '\n', '\r', '\t']:
					break;
			self.position = position
	def move(self, relative):
		return ExecutionPointer(self.id, self.position + relative)
	def search(self, pattern):
		code = storage.cells[self.id].content[self.position:]
		found = code.find(pattern)
		if found == -1:
			error(f"Sequence »{pattern}« not found in »{code}«.")
		else:
			self.position += found
	def toCode(self):
		return ' ' * self.generation + int2code(self.position) + ' ' + self.id

class Cellstorage:
	def __init__(self, main = '', parent = False):
		self.cells = {'': Cell(main), '-': Cell('stdin')}
		self.files = {'-': sys.stdin}
		self.modes = {'-':'.', '.-':'...', '--':'...'}
		self.children = {'': parent}
	def print(self):
		for addr, cell in self.cells.items():
			if not addr in ['', '-']:
				mode = self.getMode(addr)
				if mode:
					print(addr + ' :(' + mode + ') ' + cell.content)
				else:
					print(addr + ' : ' + cell.content)
	def getChild(self, id):
		if id in self.children.keys():
			return self.children[id]
		else:
			return False
	def giveBirth(self, id):
		newStorage = Cellstorage(main = self.getContent(''), parent = self)
		self.children.update({id: newStorage})
	def getMode(self, id):
		if id in self.modes.keys():
			return self.modes[id]
		else:
			#error(f"can't get mode from unexistent cell »{id}«.")
			return ''
	def setMode(self, id, mode):
		self.modes.update({id: mode})
	def exists(self, id):
		return id in self.cells.keys()
	def isFile(self, id):
		return id in self.files.keys()
	def fileHandle(self, id):
		if self.isFile(id):
			return self.files[id]
		else:
			error(f"»{id}« is no file.")
	def setFileHandle(self, id, handle):
		if self.isFile(id):
			self.files.update({id:handle})
		else:
			error(f"»{id}« is no file.")
	def createFile(self, id, name):
		if self.isFile(id):
			error(f"»{id}« already open with file »{self.getContent(id)}«.")
		else:
			self.cells.update({id:Cell(name)})
			self.modes.update({id:'.'})
			self.files.update({id:''})
	def write(self, id, cell):
		if self.getMode(id) == '...': # Special Usage of address
			if id == '.-':	# move cell to Address stack
				addressstack.push(cell)
			elif id == '--': # change morse table
				pair=cell.content.split(' ',1)
				if len(pair) < 2:
					error(f"»{pair[0]}« is no valid update for the morse table.")
				else:
					morsecodes.update({pair[0]:pair[1]})
			elif id == '.-.': # Random number
				random.seed(cell.getFloat())
			elif id == '-...': # Base for Numeric Konversion
				newBase = cell.getFloat()
				if newBase > 0 and newBase < 36:
					global base
					base = newBase
				else:
					error(f"{newBase} is no valid Base.")
			elif id == '-..': # set Date format
				global timeFormat
				timeFormat = cell.content
			else:
				error(f"no Special Usage defined for Writing address »{id}«")
				return Cell('')
		elif self.isFile(id):
			if id == '-': # stdout
				try:
					sys.stdout.write(cell.content)
				except:
					error(f"could not Write to stdout.")
			else:
				file = self.fileHandle(id)
				if file and not hasattr(file, 'mode'):
					error(f"File handle »id« is broken.")
					file = ''
				try:
					if file == '':
						file = open(self.getContent(id), 'a')
						self.setFileHandle(id, file)
					elif not ('a' in file.mode):
						pos = file.tell()
						file = open(self.getContent(id), 'a')
						self.setFileHandle(id, file)
						file.seek(pos)
					file.truncate()
					file.write(cell.content)
				except:
					error(f"failed to Write to file »{self.getContent(id)}«.")
		else: # memory
			mode = self.getMode(id)
			if mode == '': # default -> memory
				self.cells.update({id:cell})
			elif self.exists(mode): # custom usage
				global ep
				stack.push(Cell('.--')) # Write access
				# TODO do we need to check the custom handler for mode .-..?
				addressstack.push(Cell(ep.toCode())) # place return address on the address stack
				ep = ExecutionPointer(mode) # execute usage handler
			else:
				error(f"usage »{mode}« is not defined for Write.")
			
	def read(self, id):
		if self.getMode(id) == '...': # Special Usage of address
			if id == '.-':	# move cell from Address stack
				return addressstack.pop()
			elif id == '.-..': # Length of stacks
				stack.push(Cell(int2code(addressstack.size())))
				return Cell(int2code(stack.size() - 1))
			elif id == '--': # read token from position Marked on address stack
				address=addressstack.pop().content.split(' ',1)
				if len(address) < 2:
					error(f"No valid addess Marked to read from.")
					return Cell('')
				else:
					pointer = ExecutionPointer(position=code2int(address[0]), id=address[1])
					cell = Cell(pointer.getToken())
					addressstack.push(Cell(pointer.toCode()))
					return cell
			elif id == '.-.': # Random number
				tos = stack.pop()
				range1 = tos.getInt()
				if tos.len():
					range2 = tos.getInt()
					try:
						return Cell(int2code(random.randint(range1, range2)))
					except:
						error(f"illegal random number range from {range1} to {range2}")
				elif range1 == 0:
					return Cell(float2code(random.random()))
				elif range1 > 0:
					return Cell(int2code(random.randint(0, range1)))
				else:	
					error(f"random number for negative value {range1} undefined")
					return Cell('')
			elif id == '-..': # current Date/time
				return Cell(float2code(time.time()))
			elif id == '-...': # Base for Numeric Konversion
				return Cell(float2code(base))
			else:
				error(f"no Special Usage defined for address »{id}«")
				return Cell('')
		elif self.getMode(id) == '..-': # Url
			req = urllib.request.Request(self.getContent(id))
			try:
				with urllib.request.urlopen(req) as response:
					return Cell(response.read().decode("utf-8", "replace"))
			except:
				error(f"Url »{self.getContent(id)}« could not be read.")
				return Cell('')
		elif self.isFile(id):
			cell = Cell('')
			file = self.fileHandle(id)
			mode = self.getMode(id)
			if file and not hasattr(file, 'mode'):
				error(f"File handle »id« is broken.")
				file = ''
			try:
				if file == '' or not ('r' in file.mode):
					if mode == '-...':
						file = open(self.getContent(id), 'rb')
						self.setFileHandle(id, file)
					else:
						file = open(self.getContent(id), 'r')
						self.setFileHandle(id, file)
				if mode == '.': # read Everything
					cell.content = file.read()
				elif mode == '.-..': # read Linewise
					cell.content = file.readline()
				elif mode == '-': # read Token
					while not (character := file.read(1)) in endOfToken:
						cell.content += character
				elif mode == '----': # read CHaracters
					cell.content = file.read(stack.pop().getInt())
				elif mode == '-...': # read Bytes
					for i in range(stack.pop().getInt()):
						cell.content += int2code(file.read(1)[0]) + ' '
					cell.content = cell.content.strip()
				else:
					error(f"file »{self.getContent(id)}« at {id} is in mode »{mode}«.")
					return Cell('')
			except:
				error(f"could not Read from file »{self.getContent(id)}« at »{id}«.")
				return Cell('')
			return cell
		elif self.exists(id):
			global ep
			mode = self.getMode(id)
			if mode == '': # default -> memory
				return self.cells[id]
			elif self.exists(mode): # custom usage
				stack.push(Cell(id)) # custom command needs to know the address
				stack.push(Cell('')) # empty cell for read access
				# TODO do we need to check the custom handler for mode .-..?
				addressstack.push(Cell(ep.toCode())) # place return address on the address stack
				ep = ExecutionPointer(mode) # execute usage handler
				return stack.pop() # The command left the return value there
			else:
				error(f"usage »{mode}« is not defined for Read.")
				return Cell('')
		else:
			error(f"Storage »{id}« does not exist.")
			return Cell('')
	def getContent(self, id):
		if not self.exists(id):
			error(f"»{id} does not exist in storage.")
			return Cell('')
		else:
			return self.cells[id].content
		

class Cellstack:
	def __init__(self):
		self.stack = []
	def size(self):
		return len(self.stack)
	def pop(self):
		if len(self.stack):
			return self.stack.pop()
		else:
			error("Stack underrun.")
			return Cell('')
	def push(self, cell):
		self.stack.append(cell)
	def delete(self, i): # i=0 is drop, i=1 is nip, ...
		stack = self.stack
		if i < 0:
			error(f"Requesting to delete negative stack item {i}.")
		elif i >= self.size():
			error("Stack underrun.")
		else:
			del(stack[self.size() - i - 1])
	def pick(self, i): # i=0 is dup, i=1 is over, ...
		stack = self.stack
		if i < 0:
			error(f"Requesting negative stack item {i}.")
		elif i >= self.size():
			error("Stack underrun.")
			stack.append(Cell(''))
		else:
			stack.append(stack[self.size() - i - 1].copy())
	def roll(self, i): # i=1 is swap, i=2 is rot, ...
		stack = self.stack
		if i <= 0:
			error(f"Requesting to take stack item {i} to the top.")
		elif i >= self.size():
			error("Stack underrun.")
		else:
			n = self.size() - i - 1
			cell = stack[n]
			del(stack[n])
			stack.append(cell)
	def trace(self):
		for cell in reversed(self.stack):
			print(cell.content)
	def getAll(self):
		return self.stack

class Time:
	def __init__(self, code = '', timeText = ''):
		self.code = code
		if timeText: # parse date from string
			format = Cell(timeFormat)
			time = Cell(timeText)
			year = month = day = 1
			hour = minute = second = 0
			while format.len():
				token = format.getToken()
				value = ''
				if time.len():
					value = time.getToken()
				else:
					error(f"»{timeText}« too short to be passed as Date by »{timeFormat}«.")
				if token == '-.--':
					year = code2int(value)
				elif token == '--':
					month = code2int(value)
				elif token == '-..':
					day = code2int(value)
				elif token == '....':
					hour = code2int(value)
				elif token == '..':
					minute = code2int(value)
				elif token == '...':
					second = code2int(value)
			try:
				self.time = datetime.datetime(year, month, day, hour, minute, second)
				self.code = float2code(self.time.timestamp())
			except:
				error(f"illegal date {year}-{month}-{day} {hour}:{minute}:{second}.")
				self.time = datetime.datetime.fromtimestamp(0)
		else:
			try:
				self.time = datetime.datetime.fromtimestamp(code2float(self.code))
			except:
				error(f"»{self.code}« is no valid time.")
				self.time = datetime.datetime.fromtimestamp(0)
				self.code = float2code(self.time)
	def toCode(self):
		return self.code
	def getElement(self, token):
		if token == '-.--':
			return int2code(self.time.year)
		elif token == '--':
			return int2code(self.time.month)
		elif token == '-..':
			return int2code(self.time.day)
		elif token == '....':
			return int2code(self.time.hour)
		elif token == '..':
			return int2code(self.time.minute)
		elif token == '...':
			return int2code(self.time.second)
		elif token == '-.-.': # Calendar week
			return int2code(self.time.isocalendar()[1])
		elif token == '.--': # Week day
			return int2code(self.time.isocalendar()[2])
	def toString(self):
		text = ''
		mode = ''
		format = Cell(timeFormat)
		while format.len():
			token = format.getToken()
			if mode == 'T': # Text mode expects morse text and inserts escaped elements
				pass
			else:
				element = self.getElement(token)
				if element:
					if text:
						text += ' '
					text += element
		return text
def int2code(num):
	if num < 0:
		return '.' + bin(-num)[2:].replace('0','.').replace('1','-')
	else:
		return bin(num)[2:].replace('0','.').replace('1','-')
def code2int(code):
	if code == '':
		error(f"trying to convert an empty token to integer")
		return 0
	elif code == '.':
		return 0
	elif code[0] == '.':
		if code[1] == '.':
			error(f"»{code}« is no integer")
		return -int(code[1:].replace('.','0').replace('-','1'),2)
	else:
		return int(code.replace('.','0').replace('-','1'),2)
def float2code(num):
	exponent = 0
	signExp = '-'
	while num % 1:
		exponent -= 1
		num *= 16
	if exponent == 0 and num < 2**16:
		return int2code(int(num))
	while num % 16 == 0:
		exponent += 1
		num /= 16
	if exponent == 0:
		return int2code(int(num))
	elif exponent < 0:
		signExp = '.'
		exponent = - exponent
	expString = bin(exponent).replace('0b','...').replace('0','.').replace('1','-')
	expString = expString[-(len(expString) - len(expString)%4):]
	#print(f"{int(len(expString)/2)},{int2code(int(num))},{expString},{signExp}")
	return '.' * int(len(expString)/2) + int2code(int(num)) + expString + signExp
def code2float(code):
	if len(re.sub('[\\'+strokes+dots+']', '', code)):
		error(f"«{code}« is no number")
	if code == '.':
		return 0
	numstring = code
	exponentChars = 0
	while len(numstring) >= 2 and numstring[:2] == '..':
		exponentChars += 4
		numstring = numstring[2:]
	if len(numstring) < exponentChars + 1:
		error(f"»{code}« is no valid number")
		return 0
	expSign = 1
	if exponentChars:
		if numstring[-1:] == '.':
			expSign = -1
		numstring = numstring[:-1]
	else:
		return code2int(numstring)
	mantisse = code2int(numstring[:-exponentChars])
	numstring = numstring[-exponentChars:]
	exponent = expSign * code2int(numstring[numstring.index('-'):])
	#print(mantisse, exponent)
	return mantisse * 16**exponent

def error(msg):
	global ep
	pos = ep.position
	code = ep.id
	if code == '':
		code = 'main'
	if code == '.':
		#print("error in error handler")
		pass
	elif storage.exists('.'):
		addressstack.push(Cell(ep.toCode())) # place return address on the address stack
		ep = ExecutionPointer('.') # execute custom error handler
	else:
		print(f"Error at #{pos} of {code}: {msg}")
		code = storage.getContent(ep.id).strip()
		codelines = code.split('\n')
		while len(codelines) > 1 and pos > len(codelines[0]):
			pos -= len(codelines[0]) + 1
			del codelines[0]
		print(codelines[0] + '\n' + ' '*pos + '^')
		stack.trace()
		global err
		err = True

def subroutine(command):
	global ep, addressstack, storage
	addressstack.push(Cell(ep.toCode())) # place return address on the address stack
	if storage.getMode(command) == '.-..': # Use = Local
		if not storage.getChild(command):
			storage.giveBirth(command)
		storage.getChild(command).write('', storage.cells[command])
		storage = storage.getChild(command)
		for address in addressstack.getAll():
			address.content = ' ' + address.content
		command = ''
	ep = ExecutionPointer(command) # execute given command

def initGlobals(rootstorage):
	global storage
	storage = rootstorage
	global stack
	stack = Cellstack()
	global addressstack
	addressstack = Cellstack()
	global ep
	ep = ExecutionPointer('')
	global base
	base = 10
	global err
	err = False
