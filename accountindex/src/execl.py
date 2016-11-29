#coding=utf-8

from pyExcelerator import Style, Workbook, Font
import ast

#中国省份信息
provincesdict = {'11': '北京',
             '12': '天津',
             '13': '河北',
             '14': '山西',
             '15': '内蒙古',
             '21': '辽宁',
             '22': '吉林',
             '23': '黑龙江',
             '31': '上海',
             '32': '江苏',
             '33': '浙江',
             '34': '安徽',
             '35': '福建',
             '36': '江西',
             '37': '山东',
             '41': '河南',
             '42': '湖北',
             '43': '湖南',
             '44': '广东',
             '45': '广西',
             '46': '海南',
             '50': '重庆',
             '51': '四川',
             '52': '贵州',
             '53': '云南',
             '54': '西藏',
             '61': '陕西',
             '62': '甘肃',
             '63': '青海',
             '64': '宁夏',
             '65': '新疆',
             '71': '台湾',
             '81': '香港',
             '82': '澳门',
             '100': '其他',
             '400': '海外',
             '0': '其他',
             '':'', 'N/A': 'N/A'
             }

def write_excel(results):
    title = ['DATE', 'User ID', 'SCREEN NAME', 'Fans', 'Fan Growth', 'Fan Growth %', 'Tweets', 'Retweets', 'Comments', 'direct @',
                      'Likes', 'Impression', 'ER 30 days', 'ER 7 days', '#1 Post URL', '#1 Post ER', '#1 Post RT', '#1 Post CT', '#2 Post URL',
                      '#2 Post ER', '#2 Post RT', '#2 Post CT', '#3 Post URL', '#3 Post ER', '#3 Post RT', '#3 Post CT', '#4 Post URL',
                      '#4 Post ER', '#4 Post RT', '#4 Post CT', '#5 Post URL', '#5 Post ER', '#5 Post RT', '#5 Post CT', '#1 Influencer URL',
                      '#1 Influencer Tweets Count', '#1 Influencer Comments Count', '#1 Influencer Direct @ Count', '#2 Influencer URL',
                      '#2 Influencer Tweets Count', '#2 Influencer Comments', '#2 Influencer Direct @ Count', '#3 Influencer URL',
                      '#3 Influencer Tweets Count', '#3 Influencer Comments', '#3 Influencer Direct @ Count', '#4 Influencer URL',
                      '#4 Influencer Tweets Count', '#4 Influencer Comments', '#4 Influencer Direct @ Count', '#5 Influencer URL',
                      '#5 Influencer Tweets Count', '#5 Influencer Comments', '#5 Influencer Direct @ Count', '#1 Hashtag',
                      "#1 Hashtag's engagement rate", '#2 Hashtag', "#2 Hashtag's engagement rate", '#3 Hashtag',
                      "#3 Hashtag's engagement rate", 'Question Posted', 'Question Responded', 'Question Response Time', 'Response Share']
    w = Workbook()
    ws = w.add_sheet('Weekly Raw Data')
    wt = w.add_sheet('Fans Info')

    font = Font()
    font.height = 12 * 0x14
    font.name = str_to_unicode('微软雅黑')
    title_style =  Style.XFStyle()
    title_style.font = font

    fontbold = Font()
    fontbold.height = 12 * 0x14
    fontbold.bold = True
    fontbold.name = str_to_unicode('微软雅黑')
    boldstyle =  Style.XFStyle()
    boldstyle.font = fontbold

    percent = Style.XFStyle()
    percent.font = font
    percent.num_format_str = '0.00%'

    for i in range(len(title)):
        ws.col(i).width = 3600
    ws.write_cols(0, 0, title, title_style)
    abscissa = 0
    for res in range(len(results)):
        screen_name, uid, day, period, fans, fan_growth, tweets, retweets, comments, direct_at, likes, impressions, \
                   er_30, er_7, response_share, top_posts, top_influencer, top_hashtag, questions, responds, mean_res, active, interactive, \
                   verified, subfans, province, gender, age, tag, fans_week, fans_hour, brand_week, brand_hour = results[res]
        fan_percent = fan_growth / float(fans - fan_growth)
        top_posts, top_influencer, top_hashtag, verified, subfans, province, gender, age, tag, fans_week, \
                    fans_hour, brand_week, brand_hour = [format_data(p) for p in (top_posts, top_influencer, top_hashtag, \
                                                                                       verified, subfans, province, gender, age, tag, fans_week, \
                                                                                       fans_hour, brand_week, brand_hour)]
        mean_res = round(mean_res/60.0, 2)
        #print res
        t_posts = []
        top_posts = sorted(top_posts, key=lambda x:x[0], reverse=True)
        for post in top_posts:
            t_posts.extend([post[1]['url'], post[0], post[1]['nret'], post[1]['ncmt']])
        t_posts.extend(['N/A'] * (20 - len(t_posts)))

        t_influencer = []
        top_influencer = sorted(top_influencer, key=lambda x:x[0], reverse=True)
        for influ in top_influencer:
            weibourl = 'http://weibo.com/u/%s'%influ[1]['uid']
            t_influencer.extend([weibourl, influ[1].get('reposts', 0), influ[1].get('comments', 0), influ[1].get('direct_at', 0)])
        t_influencer.extend(['N/A'] * (20 - len(t_influencer)))

        t_hashtag = []
        if top_hashtag:
            top_hashtag = sorted(top_hashtag, key=lambda x:x[0], reverse=True)
            [t_hashtag.extend([hash[1], hash[0]]) for hash in top_hashtag]
        t_hashtag.extend(['N/A'] * (6 - len(t_hashtag)))

        account_index = [day.strftime('%Y-%m-%d'), uid, screen_name, fans, fan_growth, fan_percent, tweets, retweets, \
                         comments, direct_at, likes if likes else 0, \
                         impressions, er_30, er_7] + t_posts + t_influencer + t_hashtag + [questions, responds, mean_res,
                                                                                           response_share if response_share else 'N/A']
        #将第一页数据写入execl
        ws.write_cols(res+1, 0, account_index, title_style)

        tag.extend([('N/A', 0) for i in range(10 - len(tag))])
        province.extend([('N/A', 0) for i in range(10 - len(province))])
        subfans.extend([0 for i in range(12 - len(subfans))])

        vertical_title = [screen_name, 'Active', 'Active Fans', 'Other Fans', '', 'Interaction', 'Interactive Fans', 'Other Fans', '', 'Verified Type', \
         'Verified', 'Daren', 'Un-verified', '', 'Fan Number', '0~9', '10~49', '50~99', '100~199', '200~299', '300~399', '400~499',\
         '500~999', '1000~1999', '2000~4999', '5000~9999', '>=10000', '', 'Gender', 'Male', 'Female', '', 'Age', '<18', '18~24', \
         '25~29', '30~34', '35~39', '40~49', '50~59', '>=60', '', 'Tag'] + [i[0] for i in tag] + ['', 'Province'] + \
         [str_to_unicode(provincesdict.get(str(i[0]), '')) for i in province]+  ['', 'Hour', '0-1', '1-2', '2-3', '3-4', '4-5', '5-6',\
         '6-7', '7-8', '8-9', '9-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', \
         '22-23', '23-0', '', 'Days', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', '']
        wt.col(res*3).width = 4000
        ordinate = 0
        for ver in range(len(vertical_title)):
            if ver in (0, 1) or not vertical_title[ver-1]:
                wt.write(ordinate, abscissa, vertical_title[ver], boldstyle)
            else:
                wt.write(ordinate, abscissa, vertical_title[ver], title_style)
            ordinate += 1
        if verified:
            verified_count = float(sum(verified))
            verified_type = [verified[1]/verified_count, verified[2]/verified_count, verified[0]/verified_count] if verified_count > 0 else [0, 0, 0]
        else:
            verified_type = [0] * 3

        if len(gender)!=2: gender = [0, 0]
        else:
            gender.sort()
            gender = [gender[1][1], gender[0][1]]

        tagdata = [i[1] for i in tag]
        provincedata = [i[1] for i in province]
        if age:
            age = [i[1] for i in sorted(age.items())]
            age_type = [i/float(sum(age)) for i in age]
        else:
            age_type = [0] * 8

        if not brand_hour : brand_hour = [0] * 24
        if not brand_week : brand_week = [0] * 7
        subfans_type, gender_type, tag_type, province_type, fanshour_type, fansweek_type, brandhour_type, brandweek_type = \
               [div_data(j) for j in [subfans, gender, tagdata, provincedata, fans_hour, fans_week, brand_hour, brand_week]]

        gaps = ['', 'Percentage']
        vertical_data = ['', 'Percentage', active, 1-active if active else 0, '', 'Percentage', interactive, 1-interactive if interactive else 0, \
                         '', 'Percentage'] + verified_type + gaps + subfans_type + gaps + gender_type + gaps + age_type + gaps + \
                      tag_type + gaps + province_type + ['', 'Fans Activity'] + fanshour_type + ['', 'Fans Activity'] + fansweek_type

        wt.col(res*3+1).width = 4000
        ordinate = 0
        abscissa += 1
        for ver in range(len(vertical_data)):
            if ver in (0, 1) or not vertical_title[ver-1]:
                wt.write(ordinate, abscissa, vertical_data[ver], boldstyle)
            else:
                wt.write(ordinate, abscissa, vertical_data[ver], percent)
            ordinate += 1

        wt.col(res*3+2).width = 4000
        ordinate = 0
        rest_data = [''] * 66 + ['Brand Activity'] + brandhour_type + ['', 'Brand Activity'] + brandweek_type
        abscissa += 1
        for ver in range(len(rest_data)):
            if ver in (0, 1) or not vertical_title[ver-1]:
                wt.write(ordinate, abscissa, rest_data[ver], boldstyle)
            else:
                wt.write(ordinate, abscissa, rest_data[ver], percent)
            ordinate += 1
        abscissa += 2
    return w
    #try:
        #w.save('abc.xls')
    #except:
        #pass

def div_data(lista):
    #if not sum(lista):
        #print lista
    if not sum(lista):
        return lista
    return [i/float(sum(lista)) for i in lista]

def format_data(strs):
    try:
        return ast.literal_eval(strs)
    except:
        return ''

def str_to_unicode(string):
    if isinstance(string, str):
        return string.decode('utf-8')
    return string

if __name__ == "__main__":
    res = ((u'\u8499\u725b\u4e73\u4e1a', 1653196740L, '2013-9-21', u'weekly', 541867L, -4075L, 25L, 2846L, 612L, 156L, 0L, 0.000346, 0.000267, u"[(0.0024459702317865535, {'url': 'http://api.t.sina.com.cn/1653196740/statuses/3623574407232942', 'ncmt': 144L, 'nret': 1183L}), (0.000817691605032855, {'url': 'http://api.t.sina.com.cn/1653196740/statuses/3623158315546874', 'ncmt': 59L, 'nret': 385L}), (0.000303876357314396, {'url': 'http://api.t.sina.com.cn/1653196740/statuses/3623187805581993', 'ncmt': 27L, 'nret': 138L}), (0.00025599281010121845, {'url': 'http://api.t.sina.com.cn/1653196740/statuses/3623173343905657', 'ncmt': 31L, 'nret': 108L}), (0.00020257826887661143, {'url': 'http://api.t.sina.com.cn/1653196740/statuses/3623121695239392', 'ncmt': 22L, 'nret': 88L})]", u"[(22L, {'uid': 1300321563L, u'comments': 9L, u'reposts': 13L}), (20L, {'uid': 1707045601L, u'comments': 10L, u'reposts': 10L}), (17L, {'direct_at': 3L, 'uid': 2302906924L, u'comments': 6L, u'reposts': 8L}), (17L, {'direct_at': 17L, 'uid': 1823197715L}), (15L, {'direct_at': 9L, 'uid': 1094176065L, u'comments': 3L, u'reposts': 3L})]", u"[(0.0024459702317865535, u'\\u5e78\\u798f\\u649e\\u89c1YOU'), (0.000817691605032855, u'\\u58f9\\u5757\\u626b\\u973e\\uff0c\\u5411\\u7eff\\u8272\\u8fdb\\u51fb'), (0.00016038239842477842, u'\\u8499\\u725b\\u548c\\u4ed6\\u7684\\u4f19\\u4f34\\u4eec')]", 11L, 0L, 0L, 0.0, 0.0, u'[107, 2, 37]', u'[23, 24, 21, 27, 12, 3, 6, 13, 6, 5, 6]', u'[(11L, 26), (33L, 13), (32L, 12), (31L, 9), (100L, 8), (37L, 8), (400L, 7), (44L, 7), (35L, 6), (51L, 5)]', u"[(u'f', 78), (u'm', 68)]", u"''", u"[(u'\\u65c5\\u6e38', 20), (u'\\u7f8e\\u98df', 15), (u'\\u6587\\u827a', 12), (u'\\u65f6\\u5c1a', 11), (u'\\u661f\\u5ea7\\u547d\\u7406', 9), (u'\\u5065\\u5eb7', 9), (u'\\u4f53\\u80b2', 9), (u'90\\u540e', 9), (u'IT\\u6570\\u7801', 8), (u'\\u97f3\\u4e50', 6)]", u'[1314L, 294L, 1730L, 68L, 13L, 0, 18L]', u'[8L, 2L, 0L, 1L, 0L, 1L, 0L, 7L, 12L, 109L, 458L, 261L, 859L, 466L, 455L, 227L, 274L, 164L, 36L, 9L, 15L, 12L, 16L, 45L]', u'[7L, 5L, 5L, 2L, 2L, 0, 2L]', u'[0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 3L, 1L, 2L, 1L, 1L, 2L, 3L, 3L, 1L, 0L, 0L, 2L, 0L, 2L, 2L]'),)
    write_excel(res)


