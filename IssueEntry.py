from lib_text_truncate import text_truncate


class IssueEntry:

	# ------------------------------------------------------------------------------
	def __init__(self, issue, summary, story_points, sprint):
		self.issue = issue
		self.summary = summary
		self.story_points = story_points
		self.sprint = sprint

		self.short_summary = text_truncate(self.summary, 80)

	# ------------------------------------------------------------------------------
	def get_debug_info(self):
		return str(self.issue) + '|' + \
			str(self.summary) + '|' + \
			str(self.short_summary) + '|' + \
			str(self.story_points) + '|' + \
			str(self.sprint)

	# ------------------------------------------------------------------------------
	def get_as_insert_stmt(self):
		return 'INSERT INTO issue(issue,summary,short_summary,story_points,sprint) VALUES (' + \
			"'" + str(self.issue) + "'," + \
			"'" + str(self.summary).replace("'", "''") + "'," + \
			"'" + str(self.short_summary.replace("'", "''")) + "'," + \
			str(self.story_points) + "," + \
			"'" + str(self.sprint) + "');"
