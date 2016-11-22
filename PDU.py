class PDU:
    """ our data object to send via app layer protocol"""
    def __init__(self, data_raw):
    	data_split = data_raw.split('\r')

    	self.req_type = data_split[0].split()[0] 
    	self.uri = data_split[0].split()[1]
    	self.protocol_name = data_split[0].split()[2]
    	self.host_address = data_split[1].split()[1]
    	self.connection_type = data_split[2].split()[1]
    	self.content_length = data_split[3].split()[1]
    	self.origin = data_split[4].split()[1]
    	self.user_agent = "".join(data_split[5].split()[1:])
    	self.contetnt_type = data_split[6].split()[1]
    	self.accept = data_split[7].split()[1]
    	self.referer = data_split[8]
    	self.accept_encoding = data_split[9]
    	self.accept_leng = data_split[10]
    	try:
            self.content = data_split[12]
            self.content = self.content.replace("<p>", "")
            self.content = self.content.replace("</p>", "")
        except IndexError as ir:
            self.content = ""
        

    	self.data_split = data_split

    def __str__(self):
    	res = ""
    	res += self.data_split[0].split()[0] 
    	res += "\n"
    	res +=  self.data_split[0].split()[1]
    	res += "\n"
    	res +=  self.data_split[0].split()[2]
    	res += "\n"
    	res +=  self.data_split[1].split()[1]
    	res += "\n"
    	res +=  self.data_split[2].split()[1]
    	res += "\n"
    	res +=  self.data_split[3].split()[1]
    	res += "\n"
    	res +=  self.data_split[4].split()[1]
    	res += "\n"
    	res +=  "".join(self.data_split[5].split()[1:])
    	res += "\n"
    	res +=  self.data_split[6].split()[1]
    	res += "\n"
    	res +=  self.data_split[7].split()[1]
    	res += "\n"
    	res += "REF: " + self.data_split[8]
    	res += "\n"
        res += "ENC: " + self.data_split[9]
        res += "\n"
        res += "LENG: " + self.data_split[10]
        res += "\n"
        res += "CONTETNT :" + self.content
        
    	return res
    	#self.referer = data_split[8].split()[1]
    	#self.accept_encoding = data_split[9].split()[1]
    	#self.accept_leng = data_split[10].split()[1]
    	#self.content = data_split[11:]



