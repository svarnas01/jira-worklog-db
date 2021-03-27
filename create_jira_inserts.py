import os
import requests
import urllib.parse
import json
from WorklogEntry import WorklogEntry
from IssueEntry import IssueEntry

STORY_POINTS    = 'customfield_10103'
SPRINT          = 'customfield_10105'

sql_output_file = 'jira-tables-inserts.sql'
sql_start_date  = '2000/01/01'
sql_end_date    = '2021/03/25'

# ------------------------------------------------------------------------------
def api_call(remote_url):

	json_obj_list = []

	max_entries = 1000
	start_at = 0

	query_string_delim = '?'
	if remote_url.find('?') != -1:
		query_string_delim = '&'

	while True:
		response = requests.get(
			str(remote_url) +
			str(str(query_string_delim) + 'startAt=' + str(start_at) + '&maxResults=' + str(max_entries)),
			auth=('Stan.Varnas', '57Lpcustom'))

		if response.status_code != 200:
			print('response = ' + str(response.status_code))
			break

		json_str = response.content.decode('UTF-8')
		dict_obj = json.loads(json_str)
		json_obj_list.append(dict_obj)

		# print(json_str)
		# print(start_at)
		# print("\n")

		total_entries = dict_obj.get('total')
		start_at = start_at + max_entries
		if start_at > total_entries -1:
			break

	return json_obj_list

# ------------------------------------------------------------------------------

jql_str = 'project="BTMS Development" and created >= "' + sql_start_date + '" and created <= "' + sql_end_date + '"'
fields_str = '&fields=key'

remote_url = 'https://jira.modetrans.com/rest/api/2/search?' + \
		'jql=' + urllib.parse.quote_plus(jql_str) + \
		fields_str

obj_list = api_call(remote_url)

key_list=[]
for obj in obj_list:
	for issues in obj['issues']:
		key_list.append(issues['key'])

key_list.reverse()

# for key in key_list:
# 	print(key)



worklog_entry_list = []

for key in key_list:
	remote_url = 'https://jira.modetrans.com/rest/api/2/issue/' + key + '/worklog'
	#print(remote_url)
	obj_list = api_call(remote_url)



	print('=============================================')
	print(key)
	print(obj_list[0]['total'])
	for worklog in obj_list[0]['worklogs']:

		worklog_entry_list.append(WorklogEntry(
			key,
			worklog['updateAuthor']['displayName'],
			worklog['updated'],
			worklog['timeSpentSeconds']))


if os.path.exists(sql_output_file):
	os.remove(sql_output_file)

f = open(sql_output_file, "a")
for worklog_entry in worklog_entry_list:
	f.write(worklog_entry.get_as_insert_stmt() + "\n")

# ------------------------------------------------------------------------------

jql_str = 'project="BTMS Development" and created >= "' + sql_start_date + '" and created <= "' + sql_end_date + '"'
fields_str = '&fields=summary&fields=customfield_10103&fields=customfield_10105'

remote_url = 'https://jira.modetrans.com/rest/api/2/search?' + \
		'jql=' + urllib.parse.quote_plus(jql_str) + \
		fields_str

#remote_url = 'https://jira.modetrans.com/rest/api/2/issue/createmeta?projectKeys=FD&issuetypeNames=Task&expand=projects.issuetypes.fields'

obj_list = api_call(remote_url)

issue_meta_list={}
for obj in obj_list:
	for issues in obj['issues']:
		key = issues['key']
		summary = issues['fields']['summary']

		story_points = '0.0'
		if STORY_POINTS in issues['fields']:
			story_points = issues['fields'][STORY_POINTS]
			if str(story_points) == 'None':
				story_points = '0.0'

		sprint = ''
		if SPRINT in issues['fields']:
			sprint_raw_str = str(issues['fields'][SPRINT])
			if sprint_raw_str != 'None':
				sprint_name_pos = str(issues['fields'][SPRINT]).find('name=')
				start_pos = sprint_name_pos+len('name:')
				end_pos = start_pos + 8
				sprint = sprint_raw_str[start_pos:end_pos]

		issue_meta_list[str(key)] =  {'summary':str(summary),  'story_points':str(story_points), 'sprint':str(sprint)}



key_list = issue_meta_list.keys()

f = open(sql_output_file, "a")
for key in key_list:
	issueEntry = IssueEntry(key, issue_meta_list[key]['summary'], issue_meta_list[key]['story_points'], issue_meta_list[key]['sprint'])
	f.write(issueEntry.get_as_insert_stmt() + "\n")

f.close()
