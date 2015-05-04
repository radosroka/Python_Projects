# -*- coding: utf-8 -*-


class Tweet():
	"""docstring for Tweet"""

	author = unicode("")
	author_id = unicode("")
	text = unicode("")
	timestamp = unicode("")
	id = unicode("")
	urls = {}
	


	def __init__(self, id, author, author_id, text, timestamp, urls):
		self.author = author
		self.author_id = author_id
		self.text = text
		self.timestamp = timestamp
		self.id = id
		self.urls = urls
		
	def write_to_file(self, file):
		string = unicode(self.id) + "\t" + self.author + "\t" + unicode(self.author_id) + "\t" + unicode(self.text) \
		+ "\t" + unicode(self.timestamp) + "\t"

		url_list = []

		for u in self.urls:
			url_list.append( str(u) + "*" + self.urls[u][0] + "*" + self.urls[u][1])

		string += "|".join(url_list) + "\n"

		file.write(unicode(string))

	@classmethod
	def fill_from_line(cls, line):

		my_list = line.split("\t")

		if len(my_list) < 6:
			print my_list, len(my_list)
			return None

		my_list[5] = my_list[5][:-1]
		u = my_list[5].split("|")

		urls = {}

		for item in u:
			items = item.split("*")
			if len(items) is 1:
				continue
			if len(items) is not 3:
				print len(items)
				return None
			urls[items[0]] = [items[1], items[2]]

		return cls(my_list[0], my_list[1], my_list[2], my_list[3], my_list[4], urls)