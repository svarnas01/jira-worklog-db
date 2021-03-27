# This function will truncate a string up to the nearest word, but not less than max_length
def text_truncate(text, max_length):

	#  Five chars or less is invalid, too short of truncation
	if max_length <= 0:
		return ''

	if len(text) <= max_length:
		return text
	else:
		return text[0:max_length] + '...'
