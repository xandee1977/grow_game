import atexit, bisect
from cPickle import dump, load


class high_score_keeper(object):
	''' loads, saves and keeps track of a high scores list '''
	# "public" methods
	def __init__(self, filename, numentries, default):
		'''
		takes the filename where its scores should be loaded from and saved to,
		the number of entries to keep,
		and the default list to use if no scores are there.
		'''
		self.filename = filename
		self.num_entries = numentries
		# prepare default list and fix/detect human error
		default = sorted(default)
		if len(default) < self.num_entries:
			raise RuntimeError, 'default list is too short'
		elif len(default) > self.num_entries:
			default = default[:self.num_entries]
		
		self.scores = self._load_scores(self.filename, default) # list of (score, name) tuples sorted LOWEST first
		atexit.register(self._save_scores)
	
	def check_score(self, score):
		'''
		returns True if the score would make it onto the list, False otherwise
		'''
		return score > self.scores[0][0]
	
	def add_score(self, score, name):
		''' adds the score with name to the list '''
		bisect.insort_left(self.scores, (score, name))
		del self.scores[0] # keep list at correct number of entries
	
	def get_scores(self):
		'''
		yields the entries of the list in (score, name) tuples
		from highest score to lowest
		'''
		for entry in reversed(self.scores):
			yield entry
	
	# "private" methods
	def _load_scores(self, filename, default):
		'''
		Loads the pickled score list out of filename and returns it.
		If the filename cannot be found the default high scores list is returned.
		'''
		try:
			File = open(self.filename, 'rb')
		except IOError:
			return default
		try:
			scoreslist = load(File)
		finally:
			File.close()
		# validate
		scoreslist = sorted(scoreslist)
		if len(scoreslist) < self.num_entries:
			raise RuntimeError, 'loaded scores list is too short'
		elif len(scoreslist) > self.num_entries:
			scoreslist = scoreslist[:self.num_entries]
		
		return scoreslist
	
	def _save_scores(self):
		''' saves the pickled list of scores to self.filename '''
		File = open(self.filename, 'wb')
		try:
			dump(self.scores, File, 2)
		finally:
			File.close()
