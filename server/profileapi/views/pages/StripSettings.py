class StripSettings:
	# Simple list with a bunch of.. 'safe' html tags
	ALLOWED_TAGS = [
		'a',
		'abbr',
		'acronym',
		'b',
		'blockquote',
		'code',
		'em',
		'i',
		'li',
		'ol',
		'strong',
		'ul',
		'p',
		'span',
		'div',
		'img',
		'h1',
		'h2',
		'h3',
		'h4',
		'h5'
	]

	# Like the above, but 'safe' attributes
	ALLOWED_ATTRIBUTES = {
		'a': ['href', 'title'],
		'abbr': ['title'],
		'acronym': ['title'],
		'img': ['src'],
		'*': ['class']
	}

	# Like the above, but safe styles. Mmmmmyup.

	ALLOWED_STYLES = []


