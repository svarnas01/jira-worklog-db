class WorklogEntry:

	# ------------------------------------------------------------------------------
	def __init__(self, issue, name, update_ts, work_time_secs):
		self.issue = issue
		self.name = name
		self.update_ts = update_ts
		self.work_time_secs = work_time_secs

		name_elem_list = self.name.strip().lower().replace('-', ' ').split(' ')

		self.short_name = ''
		len_name_elem_list = len(name_elem_list)
		if (len_name_elem_list > 1):
			for elem_idx in range(0, len_name_elem_list-1):
				self.short_name = self.short_name + str(name_elem_list[elem_idx][0])

		self.short_name = self.short_name + name_elem_list[len_name_elem_list-1]

	# ------------------------------------------------------------------------------
	def get_debug_info(self):
		return str(self.issue) + '|' + \
			str(self.name) + '|' + \
			str(self.short_name) + '|' +\
			str(self.update_ts) + '|' +\
			str(self.work_time_secs)

	# ------------------------------------------------------------------------------
	def get_as_insert_stmt(self):

		return 'INSERT INTO worklog(issue,username,short_username,last_updated,work_seconds) VALUES (' + \
			"'" + str(self.issue) + "'," + \
			"'" + str(self.name) + "'," + \
			"'" + str(self.short_name) + "'," + \
			"'" + str(self.update_ts) + "'," + \
			str(self.work_time_secs) + ");"

		# VALUES('FD-8157', 'Abdel Said', 'asaid', '2020-11-24T23:19:52.762+0000', 2700);
		#
		# return str(self.issue) + '|' + \
		# 	str(self.name) + '|' + \
		# 	str(self.short_name) + '|' +\
		# 	str(self.update_ts) + '|' +\
		# 	str(self.work_time_secs)
