import requests
from operator import itemgetter
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# 执行API并存储响应
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print('Status code:',r.status_code)

# 处理有关每篇文章的信息
submissions_ids = r.json()
names = []
submissions_dicts = []
status = 0
for submission_id in submissions_ids[:30]:
	url = ('https://hacker-news.firebaseio.com/v0/item/'+str(submission_id)+'.json')
	submission_r = requests.get(url)
	if submission_r.status_code:
		status = status+1
	response_dict = submission_r.json()
	names.append(response_dict['title'])
	submission_dict = {
	'value':response_dict.get('descendants',0),
	'label':response_dict['title'],
	'xlink':'https://news.ycombinator.com/item?id='+str(submission_id)
	}
	submissions_dicts.append(submission_dict) 
print(status)
print('/n'+'There titles are as follows:')
for name in names:
	print(name)
submissions_dicts = sorted(submissions_dicts,key=itemgetter('value'),
reverse=True)

# 可视化
my_style = LS('#009922',base_style = LCS)

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart  = pygal.Bar(my_config,show_legend=False)
chart.title = 'Most-Starred Python Projects on Hacker-news'
chart.x_labels = names

chart.add('',submissions_dicts)
chart.render_to_file('python_submissions.svg')
# 输出排名靠前的文章
#for submission in submissions_dicts:
#	print("/nTitle:",submission['label'])
#	print("Discussion link:",submission['xlink'])
#	print("Comments:",submission['value'])
