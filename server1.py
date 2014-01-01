from flask import Flask, request
import httplib

class FlaskPeer(object):
	
	
	def __init__(self):
		self.app = Flask(__name__)
		self.peers = []
		self.potocolVer = '0100'
	def m00(self, dat):
		pass
	def m10(self, dat):
		pass
	def m20(self, dat):
		pass
	def m30(self, dat):
		pass
	def m40(self, dat):
		pass
	def m41(self, dat):
		pass
	def runServer(self):
		@self.app.route('/<string:message>')
		def readMassage(message):
			while len(message)>5:
				key = message[:2]
				if not key in ['40']: # 40 massage has 2 byte long length param.
					data = message[4:(int(message[2:4],16)*2 +4)]
					if key in ['00' , '10', '20', '30', '41']: # protocol error
						return ''
					if key == '00':
						m00(data)
					elif key == '10':
						m10(data)
					elif key == '20':
						m20(data)
					elif key == '30':
						m30(data)
					elif key == '41':
						m41(data)
					message = message[(int(message[2:4],16)*2 +4):]
					continue
				data = message[6:(int(message[2:6],16)*2 +6)]
				m40(data)
				message = message[(int(message[2:6],16)*2 +6):]

			return ''
		self.app.run(debug=True)

if __name__=='__main__':
	server=FlaskPeer()
	server.runServer()
