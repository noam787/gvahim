from flask import Flask
import httplib

class FlaskPeer(object):
	
	
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.app = Flask(__name__)
		self.peers = []
		self.potocolVer = '0101'
		self.dests = { }
		self.sourceAddr = ''
		self.message = ''

	def m00(self, dat):
		pass
	def m10(self, dat):
		if self.ip in self.dests:
			if not dat == self.protocolVer:
				pass
	def m20(self, dat):
		if not self.dests == {}:   #send message
			if self.ip in self.dests.keys():
				del self.dests[self.ip]
			for key in self.dests:
				conn = httplib.HTTPConnection(key + ':' + self.dests[key])
				conn.request('GET','/' + self.message)
			self.dests = {}
			self.message = ''
		ttl = dat[:2]
		self.sourceAddr = dat[2:10]
		port = [10:12]
		numOfDest = int(dat[12:14],16)
		addrs = dat[14:]
		for i in range(numOfDest):
			parsedAddr= addrs[i*8:(i+1)*8]
			parsedPort =addrs[ (numOfDest*8 + i*4) : (numOfDest*8 + (i + 1)*4) ]
			self.dests[parsedAddr] = parsedPort
		
	def m30(self, dat):
		pass
	def m40(self, dat):
		pass
	def m41(self, dat):
		pass
	def runServer(self):
		@self.app.route('/<string:message>')
		def readMassage(message):
			self.message = ''				
			self.dests = {}
			while len(message)>5: # shortest message in the protocol is 6 chars long
				key = message[:2]
				if not key in ['40']: # 40 massage has 2 byte long length param.
					data = message[4:(int(message[2:4],16)*2 +4)] # splits the message from the rest of the string by len 
					if key in ['00' , '10', '20', '30', '41']: # protocol error
						return ''
					if key == '00':  # status message
						m00(data)
					elif key == '10':  # protocol message
						m10(data)
					elif key == '20':  # routing message
						m20(data)
					elif key == '30':  
						m30(data)
					elif key == '41':  # data message
						m41(data)
					message = message[(int(message[2:4],16)*2 +4):]
					continue
				data = message[6:(int(message[2:6],16)*2 +6)]
				m40(data)  #  data request
				message = message[(int(message[2:6],16)*2 +6):]
			if self.ip in self.dests.keys():
				del self.dests[self.ip]
			for key in self.dests:
				conn = httplib.HTTPConnection(key + ':' + self.dests[key])
				conn.request('GET','/' + self.message)
			return ''
		self.app.run(debug = True, host = self.ip, port = self.port)

if __name__=='__main__':
	server=FlaskPeer('localhost',5000)
	server.runServer()
