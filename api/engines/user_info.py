class GamesStatistic:
    def __init__(self, name, quantity, rating, rd, prog, prov=None):
        self.name = name
        self.quantity = quantity
        self.rating = rating
        self.rd = rd
        self.prog = prog
        self.prov = prov


class UserInfo:
    def __init__(self, info_dict):
        self.completion_rate = info_dict.get('completionRate')
        self.created_at = info_dict.get('createdAt')
        self.user_id = info_dict.get('id')
        self.language = info_dict.get('language')
        self.followers = info_dict.get('nbFollowers')
        self.following = info_dict.get('nbFollowing')
        self.online = info_dict.get('online')
        self.patron = info_dict.get('patron')

        perfs = info_dict.get('perfs', None)
        self.perfs = self.get_games_statistic_from_dict(perfs)

        play_time = info_dict.get('playTime', {})
        self.total_play_time = play_time.get('total', None)
        self.tv_play_time = play_time.get('tv', None)
        self.playing = info_dict.get('playing', None)

        profile = info_dict.get('profile', {})
        self.bio = profile.get('bio', None)
        self.country = profile.get('country', None)
        self.first_name = profile.get('firstName', None)
        self.last_name = profile.get('lastName', None)
        self.links = profile.get('links', None)
        self.location = profile.get('location', None)

        self.seen_at = info_dict.get('seenAt')
        self.url = info_dict.get('url')
        self.username = info_dict.get('username')

    def get_games_statistic_from_dict(self, info):
        games = []
        for key, value in info.items():
            games.append(GamesStatistic(name=key,
                                        quantity=value.get('games'),
                                        rating=value.get('rating'),
                                        rd=value.get('rd'),
                                        prog=value.get('prog'),
                                        prov=value.get('prov', None)
                                        ))
        return games

    def get_games_rate_html(self):
        html_template = '<b>%s</b>: %s \n'
        if self.perfs:
            lines = [html_template % (perf.name, perf.rating) for perf in self.perfs]
            return ''.join(lines)
        return ''

    def get_info_html(self):
        info = 'Online: %s \n' % self.online
        info += 'Language: %s \n' % self.language
        info += 'Link: <a href="%s">Click</a> \n' % self.url
        return info

    def get_total_info(self):
        username = '<b>%s</b>\n' % self.username
        separator = '-' * 40 + '\n'
        return username + self.get_info_html() + separator + self.get_games_rate_html()



