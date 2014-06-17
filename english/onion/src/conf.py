# coding=utf-8
import re

g_noncsdiv = u'[^\u4e00-\u9fa5]+'
g_nonendiv = u'[^\w]+'
mostused = set(u'的一了是在人不有中')
# matching a url is complex, just to simplify here
SPECIAL_PATTERN = re.compile(
    ur'(#.+?#|\[.+?\]|https?:\/\/[.\/\w$&_-]+|@[0-9a-zA-Z\u4e00-\u9fa5_-]+)')


UPLOAD_LIMIT = 10 ** 7
MAX_RATIO = 1e4

Sample_article = ('sample.txt',
"""Although born to the ease of plantation life, waited on hand and foot since infancy, the faces of the three on the porch were neither slack nor soft. They had the vigor and alertness of country people who have spent all their lives in the open and troubled their heads very little with dull things in books. Life in the north Georgia county of Clayton was still new and, according to the standards of Augusta, Savannah and Charleston, a little crude. The more sedate and older sections of the South looked down their noses at the up-country Georgians, but here in north Georgia, a lack of the niceties of classical education carried no shame, provided a man was smart in the things that mattered. And raising good cotton, riding well, shooting straight, dancing lightly, squiring the ladies with elegance and carrying one’s liquor like a gentleman were the things that mattered.

　In these accomplishments the twins excelled, and they were equally outstanding in their notorious inability to learn anything contained between the covers of books. Their family had more money, more horses, more slaves than any one else in the County, but the boys had less grammar than most of their poor Cracker neighbors.

　It was for this precise reason that Stuart and Brent were idling on the porch of Tara this April afternoon. They had just been expelled from the University of Georgia, the fourth university that had thrown them out in two years; and their older brothers, Tom and Boyd, had come home with them, because they refused to remain at an institution where the twins were not welcome. Stuart and Brent considered their latest expulsion a fine joke, and Scarlett, who had not willingly opened a book since leaving the Fayetteville Female Academy"""
)
