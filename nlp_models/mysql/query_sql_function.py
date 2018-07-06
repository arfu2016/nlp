import functools
import json
import time
import logging
import aiball.utils as utils
from aiball.db.cmysql import do_query_local_cache


def _get_support_competitions_str():
    try:
        return str(tuple(utils.get_support_competitions()))
    except Exception as e:
        logging.exception(e)
        return "(8)"


# league.py
def get_goal_rank_sql(current_season_id, league_id):
    # mysql_app = Mysql("db_service_fd")
    # mysql_app.connect_mysql()
    sql1 = '''select shirtnumber, r_position_name, r_team_name, r_person_name,
              goals, penalty_goals, minutes_played, person_id
              from squad_statistics where
              season_id = (select season_id from rlat_opta_season where
              gsm_season_id = %d) and competition_id = (select competition_id
              from rlat_opta_competition where gsm_competition_id = %d)
              order by goals desc limit 5 ''' % (current_season_id, league_id)

    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql1, ex=3600)


def get_assist_rank_sql(current_season_id, league_id):
    sql1 = '''select shirtnumber, r_position_name, r_team_name,
              r_person_name, assists, penalty_goals, minutes_played, person_id
              from squad_statistics where season_id = (select season_id
              from rlat_opta_season where gsm_season_id = %d) and
              competition_id = (select competition_id from
              rlat_opta_competition where gsm_competition_id = %d)
              order by assists desc limit 5 ''' % (
        current_season_id, league_id)
    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql1, ex=3600)


def get_season_shirtnumber_sql(current_season_id):
    sql1 = '''select person_id, shirtnumber from squad_statistics where
              season_id = (select season_id from rlat_opta_season
              where gsm_season_id = %d) ''' % current_season_id
    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql1, ex=3600)


def team_history_statistics_sql(current_season_id):
    sql1 = '''select team_id, matches_total, matches_won, matches_draw,
              matches_lost, goals_pro, goals_against, goals_clear,
              won_percent, draw_percent, lost_percent,
              yellow_cards as avg_yellow_cards, red_cards as avg_red_cards,
              corners as avg_corners,
              goals_pro/matches_total AS avg_goals_pro,
              goals_against/matches_total AS avg_goals_against,
              corners * matches_total as total_corners,
              red_cards * matches_total as total_red_cards,
              yellow_cards * matches_total as total_yellow_cards,
              goals_clear/matches_total AS avg_goals_clear
              from team_statistics where season_id = (select season_id
              from rlat_opta_season where gsm_season_id = %d )
              and type = "total" ''' % current_season_id
    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql1, ex=3600)


def get_squad_sql(season_id, team_id):
    sql1 = '''select a.person_id, a.cn_name, a.date_of_birth, a.r_position_name,
              b.shirtnumber from (select person_id, cn_name, date_of_birth,
              r_position_name from squad where person_id in (select person_id
              from rlat_team_squad where season_id=%d and team_id=%d and
              deleted=0 ) and type = "player")  as a left join(select person_id,
              shirtnumber from squad_statistics where person_id in (
              select person_id from rlat_team_squad where season_id=%d and
              team_id=%d and deleted=0) and season_id=%d and team_id=%d) as b on
              a.person_id = b.person_id WHERE b.shirtnumber != "" ''' % (
        season_id, team_id, season_id, team_id, season_id, team_id)
    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql1, ex=3600)


def get_gsm_team_id_sql(team_id):
    sql = '''SELECT gsm_team_id FROM rlat_opta_team WHERE team_id = %d ''' % team_id
    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql, ex=3600)


def get_data_center_season_id_sql(current_season_id):
    sql = '''select season_id from rlat_opta_season where
                     gsm_season_id = %d''' % current_season_id
    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql, ex=3600)


def get_league_goal_sql(current_season_id, league_id):
    sql1 = '''select sum(fs_A) as sum_home, sum(fs_B) as sum_away,
              count(*) as freq from `match` where season_id = (
              select season_id from rlat_opta_season where
              gsm_season_id = %d) and competition_id = (select
              competition_id from rlat_opta_competition where
              gsm_competition_id = %d) and `status` = "Played"
              ''' % (current_season_id, league_id)
    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql1, ex=3600)


def get_data_center_team_id_sql(gsm_team_id):
    sql = '''select team_id from rlat_opta_team where
                     gsm_team_id = %d''' % gsm_team_id
    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql, ex=3600)


# team.py


def get_status_23_msg_sql(period_time, team_id):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time.time()))
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',
                               time.localtime(
                                   time.time() - period_time * 60))
    sql = '''SELECT gsm_match_id, score, home_name, away_name, status, minute
             FROM dtb_full_gsm_match WHERE status in (2,3) and
             (home_team_id = %d or away_team_id = %d ) and match_time BETWEEN
             "%s" AND "%s" order by match_time desc limit 1 ''' % (
        team_id, team_id, start_time, current_time)
    return do_query_local_cache(
        db_name="db_gsm_app",
        db_cfg="db_gsm_app",
        sql=sql, ex=3600)


def get_game_sql(period_time, team_id):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',
                               time.localtime(time.time() -
                                              period_time * 60 * 60 * 24))
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',
                             time.localtime(time.time() +
                                            period_time * 60 * 60 * 24))
    sql = '''SELECT gsm_match_id, match_time, status FROM dtb_full_gsm_match
             WHERE (home_team_id = %d or away_team_id = %d ) and match_time
             BETWEEN "%s" AND "%s" and gsm_league_id in %s and status in
             (1, 2, 3) ''' % (team_id, team_id, start_time, end_time,
                              _get_support_competitions_str())
    return do_query_local_cache(
        db_name="db_gsm_app",
        db_cfg="db_gsm_app",
        sql=sql, ex=3600)


# match.py


def get_fixtures_sql(period_time, league_id, team_id, home_away):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time.time() - 3 * 3600))
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',
                             time.localtime(
                                 time.time() + period_time * 60))
    if league_id is not None:
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 score, home_name, away_name, home_team_id, away_team_id,
                 status, minute FROM dtb_full_gsm_match WHERE gsm_league_id = %d
                 and status in (1,3) and match_time BETWEEN "%s" AND "%s" ''' \
              % (league_id, current_time, end_time)
    elif team_id is not None and home_away == 'home':
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 score, home_name, away_name, home_team_id, away_team_id,
                 status, minute FROM dtb_full_gsm_match WHERE gsm_league_id in
                 %s  and status in (1,3) and home_team_id = %d and match_time
                 BETWEEN "%s" AND "%s" ''' % (_get_support_competitions_str(), team_id,
                                              current_time, end_time)
    elif team_id is not None and home_away == 'away':
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 score, home_name, away_name, home_team_id, away_team_id, status,
                 minute FROM dtb_full_gsm_match WHERE gsm_league_id in %s  and
                 status in (1,3) and away_team_id = %d and match_time BETWEEN
                 "%s" AND "%s" ''' % (_get_support_competitions_str(), team_id, current_time,
                                      end_time)
    elif team_id is not None and home_away == 'all':
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 score, home_name, away_name, home_team_id, away_team_id,
                 status, minute FROM dtb_full_gsm_match WHERE gsm_league_id in
                 %s  and status in (1,3) and ( home_team_id = %d or away_team_id
                 = %d ) and match_time BETWEEN "%s" AND "%s" ''' % (
            _get_support_competitions_str(), team_id, team_id, current_time, end_time)
    else:
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 score, home_name, away_name, home_team_id, away_team_id, status,
                 minute FROM dtb_full_gsm_match WHERE gsm_league_id in %s and
                 status in (1,3) and match_time BETWEEN "%s" AND "%s" ''' % (
            _get_support_competitions_str(), current_time, end_time)
    return do_query_local_cache(
        db_name="db_gsm_app",
        db_cfg="db_gsm_app",
        sql=sql, ex=3600)


def get_fixtures_one_sql(period_time, league_id, team_id, home_away):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time.time()))
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',
                             time.localtime(time.time() + period_time * 60))
    if league_id is not None:
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 home_name, away_name, home_team_id, away_team_id
                 FROM dtb_full_gsm_match WHERE gsm_league_id = %d and
                 status = 1 and match_time BETWEEN "%s" AND "%s"
                 order by match_time ''' % (league_id, current_time, end_time)
    elif team_id is not None and home_away == 'home':
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 home_name, away_name, home_team_id, away_team_id FROM
                 dtb_full_gsm_match WHERE gsm_league_id in %s  and status = 1
                 and home_team_id = %s and match_time BETWEEN "%s" AND "%s"
                 order by match_time ''' % (_get_support_competitions_str(), team_id,
                                            current_time, end_time)
    elif team_id is not None and home_away == 'away':
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 home_name, away_name, home_team_id, away_team_id FROM
                 dtb_full_gsm_match WHERE gsm_league_id in %s  and status = 1
                 and away_team_id = %s and match_time BETWEEN "%s" AND "%s"
                 order by match_time ''' % (_get_support_competitions_str(), team_id,
                                            current_time, end_time)
    elif team_id is not None and home_away is None:
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 home_name, away_name, home_team_id, away_team_id FROM
                 dtb_full_gsm_match WHERE gsm_league_id in %s  and status = 1
                 and ( home_team_id = %s or away_team_id = %s ) and match_time
                 BETWEEN "%s" AND "%s" order by match_time ''' % (
            _get_support_competitions_str(), team_id, team_id, current_time, end_time)
    else:
        sql = '''SELECT gsm_match_id, gsm_league_id, league_name, match_time,
                 home_name, away_name, home_team_id, away_team_id FROM
                 dtb_full_gsm_match WHERE gsm_league_id in %s  and status = 1
                 and match_time BETWEEN "%s" AND "%s" order by match_time''' % (
            _get_support_competitions_str(), current_time, end_time)
    return do_query_local_cache(
        db_name="db_gsm_app",
        db_cfg="db_gsm_app",
        sql=sql, ex=3600)

# player.py


def get_season_team_sql(gsm_person_id):
    sql = '''select season_id, team_id, person_id from rlat_team_squad
             where season_id=(select season_id from competition where season_id
             in (select season_id from rlat_team_squad where person_id=(select
             person_id from rlat_opta_squad where gsm_person_id=%d) and
             deleted=0) and competition_id in (select competition_id from
             rlat_opta_competition where gsm_competition_id in
             (7, 8, 9, 13, 16, 51))) and person_id=(select person_id from
             rlat_opta_squad where gsm_person_id=%d) ''' % (
        gsm_person_id, gsm_person_id)
    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql, ex=3600)


def get_player_tech_sql(season_id, team_id, person_id):
    sql = """select lineups, appearances, goals, penalty_goals, assists
             from squad_statistics where season_id=%d and team_id=%d
             and person_id=%d """ % (season_id, team_id, person_id)

    sql2 = """select gsm_team_id from rlat_opta_team where
              team_id=%d """ % team_id

    results = do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql, ex=3600)
    results2 = do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql2, ex=3600)

    return results, results2


def get_player_name_sql(gsm_person_id):
    sql = '''SELECT cn_name FROM squad WHERE person_id = (SELECT person_id FROM
             rlat_opta_squad WHERE gsm_person_id = %d) ''' % gsm_person_id

    return do_query_local_cache(
        db_name="db_service_fd",
        db_cfg="db_service_fd",
        sql=sql, ex=3600)


def get_user_fav_match_list(user_id: str) -> list:
    sql = """
    SELECT `match_id` FROM `match_care` WHERE `match_care`.`user_id`=%s
    AND `match_care`.`deleted_at` IS NULL
    """ % str(user_id)

    return do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=sql, ex=5)


def get_manager_selected_match_list() -> list:
    sql = """
    SELECT `match_id` FROM `match_manage` WHERE `match_manage`.`selection`=1
    AND `match_manage`.`deleted_at` IS NULL
    """
    return do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=sql, ex=5)


def mysql_news_get_news(news_ids_excluded: list = list()) -> list:
    sql = """
    SELECT
    `content_pool`.`id`,
    `content_pool`.`title`,
    `content_pool`.`content`,
    `content_pool`.`pre_pic`,
    `news_recommend`.`news_id`,
    `news_recommend`.`rank` 
    FROM `content_pool`
    INNER JOIN `news_recommend`
    ON `content_pool`.`id` = `news_recommend`.`news_id`
    WHERE `news_recommend`.`deleted_at` IS NULL
    AND `content_pool`.`deleted_at` IS NULL
    """

    if news_ids_excluded:
        sql += " AND `news_recommend`.`news_id` NOT IN (%s)" % \
               ",".join([str(nid) for nid in news_ids_excluded])
    sql += " ORDER BY `news_recommend`.`rank`"

    return do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=sql, ex=60)


def mysql_news_filtered_news(
        league_ids: list, team_ids: list, person_ids: list = list()) -> list:
    sql = """
    SELECT
    `content_pool`.`id` AS `news_id`,
    `content_pool`.`title` AS `news_title`,
    `content_pool`.`content` AS `news_content`,
    `content_pool`.`pre_pic` AS `pictures`,
    `news_tags_pool`.`league_id` AS `league_id`,
    `news_tags_pool`.`team_id` AS `team_id`,
    `news_tags_pool`.`player_id` AS `player_id`,
    `content_pool`.`tag` AS `tag`
    FROM `content_pool`
    INNER JOIN `news_tags_pool`
    ON `content_pool`.`id` = `news_tags_pool`.`news_id`
    AND `news_tags_pool`.`deleted_at` IS NULL
    AND `content_pool`.deleted_at IS NULL
    """

    if league_ids:
        sql += " AND `league_id` in (%s)" % ",".join(
            [str(lid) for lid in league_ids])
    if team_ids:
        sql += " AND `team_id` in (%s)" % ",".join(
            [str(tid) for tid in team_ids])
    if person_ids:
        sql += " AND `player_id` in (%s)" % ",".join(
            [str(pid) for pid in person_ids])

    sql += " GROUP BY `content_pool`.`id` ORDER BY `content_pool`.`id` DESC"
    return do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=sql, ex=60)


def myqsl_news_filtered_news_with_tag(tag: str) -> list:
    """

    :param tag:
    :return:
    """

    sql = """
    SELECT
    `content_pool`.`id` AS `news_id`,
    `content_pool`.`title` AS `news_title`,
    `content_pool`.`content` AS `news_content`,
    `content_pool`.`pre_pic` AS `pictures`,
    `content_pool`.`tag` AS `tag`
    FROM `content_pool`
    WHERE `content_pool`.`tag` = "%s"
    AND `content_pool`.deleted_at IS NULL
    GROUP BY `content_pool`.`id` ORDER BY `content_pool`.`id` DESC
    """ % tag
    return do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=sql, ex=60)


def mysql_get_terms() -> list:
    sql = """
    SELECT
    `robot_term2`.`id` AS `id`,
    `robot_term2`.`intention_number` AS `intent_id`,
    `robot_term2`.`term_type` AS `type`,
    `robot_term2`.`term_content` AS `content`,
    `robot_intention`.`intention_name` AS `intention_name`
    FROM `robot_term2`
    INNER JOIN `robot_intention`
    ON `robot_term2`.`intention_number` = `robot_intention`.`intention_number`
    """

    return do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=sql, ex=60)


def mysql_get_regex() -> list:
    sql = """
    SELECT
    `robot_reg_exp`.`id` AS `id`,
    `robot_reg_exp`.`intention_number` AS `intention_number`,
    `robot_reg_exp`.`regexp` AS `regexp`,
    `robot_reg_exp`.`power` AS `power`,
    `robot_reg_exp`.`sort` AS `sort`,
    `robot_reg_exp`.`status` AS `status`,
    `robot_reg_exp`.`flag` AS `flag`,
    `robot_reg_exp`.`scene` AS `scene`,
    `robot_intention`.`intention_name` AS `intention_name`
    FROM `robot_reg_exp`
    INNER JOIN `robot_intention`
    ON `robot_reg_exp`.`intention_number` = 
    `robot_intention`.`intention_number`
    ORDER BY `robot_reg_exp`.`sort` DESC
    """

    return do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=sql, ex=60)


def mysql_get_promotion_time_and_match(
        promotion_id: int = 0) -> (int, int, int):
    """
    根据活动id查询活动基本信息
    :param promotion_id: 活动id
    :return: 开启时间，结束时间，比赛id
    """

    return 0, 0, 0


def mysql_team_leader_by_match_id_dynamic(match_id: int) -> (int, int):
    """
    根据比赛id查询球队队长——动态数据。

    动态数据为比赛临时调整数据，优先级高于静态数据
    :return: 返回查询到的主客队队长id的元组
    """
    try:
        sql = """
        SELECT `home_team_leader_id`, `guest_team_leader_id`
        FROM `robot_team_leader` WHERE `match_id`=%d
        """ % match_id

        contents = do_query_local_cache(
            db_name="db_robot",
            db_cfg="mysql.master",
            sql=sql, ex=600)

        if contents:
            return int(contents[0][0]), int(contents[0][1])
    except Exception as e:
        logging.exception(e)
    return 0, 0


def mysql_get_ai_news(content_pool_id: int = -1, order_id: int = 0) -> tuple:
    """
    根据指定的content_pool_id和order_id获取指定的互动新闻“段”
    :param content_pool_id: 指定的互动新闻的"篇"的id
    :param order_id: 指定互动新闻的"段"的id
    :return: 返回查询到的互动新闻的段或None
    """
    _sql = """
        SELECT 
          `robot_ai_news`.`id`,
          `robot_ai_news`.`content_pool_id`,
          `robot_ai_news`.`content`,
          `robot_ai_news`.`content_type`,
          `robot_ai_news`.`media_type`,
          `robot_ai_news`.`img`,
          `robot_ai_news`.`compress_img`,
          `robot_ai_news`.`media_id`,
          `robot_ai_news`.`order`,
          `news_recommend`.`rank`
        FROM `robot_ai_news` INNER JOIN `news_recommend`
        ON `robot_ai_news`.`content_pool_id`= `news_recommend`.`news_id`
        WHERE `robot_ai_news`.`deleted_at` IS NULL
        AND `news_recommend`.`deleted_at` IS NULL
        AND `robot_ai_news`.`order` = %d
    """ % order_id

    if content_pool_id != -1:
        _sql += " AND content_pool_id=%d" % content_pool_id
    else:
        _sql += " ORDER BY `rank` LIMIT 1"

    contents = do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=_sql, ex=60)

    return contents[0] if contents else None


def mysql_get_ai_news_button_by_news_id(ai_news_id: int) -> list:
    try:
        _sql = """
        SELECT 
        `robot_ai_btn`.id,
        `robot_ai_btn`.ai_news_id,
        `robot_ai_btn`.content_pool_id,
        `robot_ai_btn`.btn_type,
        `robot_ai_btn`.btn_pic,
        `robot_ai_btn`.btn_content,
        `robot_ai_btn`.word_id,
        `robot_ai_btn`.word_content,
        `robot_ai_btn`.btn_order
        FROM robot_ai_btn
        WHERE robot_ai_btn.deleted_at IS NULL
        AND `robot_ai_btn`.ai_news_id = %d
        ORDER BY `robot_ai_btn`.btn_order, `robot_ai_btn`.btn_type
        """ % ai_news_id

        contents = do_query_local_cache(
            db_name="db_robot",
            db_cfg="mysql.master",
            sql=_sql, ex=60)
        return contents
    except Exception as e:
        logging.exception(e)
        return list()


def get_next_content_pool_id(content_pool_id: int = -1) -> int:
    """
    根据当前content_pool_id计算下一个content_pool_id
    计算规则： 先根据rank排序，rank值相同则根据id排序
    :param content_pool_id:
    :return: -1代表没有下一篇, -2代表查询不到值
    """
    sql = """
         SELECT content_pool_id FROM robot_ai_news INNER JOIN news_recommend
         ON robot_ai_news.content_pool_id = news_recommend.news_id
         GROUP BY content_pool_id
         ORDER BY news_recommend.rank, news_recommend.id
    """
    results = do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=sql, ex=5)

    if results:
        result = [res[0] for res in results]
        if content_pool_id == -1:
            return result[0]
        else:
            for i, value in enumerate(result):
                if value == content_pool_id:
                    if i != len(result) - 1:
                        return result[i + 1]
                    else:
                        return -1
    else:
        return -2


def get_next_order_id(content_pool_id: int = -1, order: int = 0) -> int:
    """
    根据content_pool_id和order计算指定篇的新闻的下一个order
    :param content_pool_id:
    :param order:
    :return: -1代表没有下一段，-2代表查询不到值,-3代表content_pool_id没有传值
    """
    if content_pool_id == -1:
        return -3
    else:
        sql = """
            select `order` from robot_ai_news 
            where content_pool_id = %s order by `order`
        """ % content_pool_id
        results = do_query_local_cache(
            db_name="db_robot",
            db_cfg="mysql.master",
            sql=sql, ex=5)

        if results:
            result = [res[0] for res in results]
            for i, value in enumerate(result):
                if value == order:
                    if i != len(result) - 1:
                        return result[i + 1]
                    else:
                        return -1
        else:
            return -2


def get_inner_content_img(_img: str = "", _compress_img: str = "") -> dict:
    """
    根据img和compress_img给出2050协议的封装
    :param _img:
    :param _compress_img:
    :return:
    """
    return {
        "code": 2050,
        "ssid": 0,
        "broadcast": 0,
        "sub_code": 0,
        "msg": "",
        "seq": "",
        "question": "",
        "power": 4,
        "time": 1517479298,
        "scene": 1,
        "minute": "null",
        "data": {
            "away_name": "",
            "away_team_id": 0,
            "count": 1,
            "home_name": "",
            "home_team_id": 0,
            "link": [{
                "compress_img": _compress_img,
                "img": _img
            }],
            "season_id": 0,
            "type": 1
        }
    }


def get_inner_content(_content: str = "", _link="") -> dict:
    """
    根据content内容返回2049协议
    :param _content:
    :param _link
    :return:
    """
    return {
        'answered': 1,
        'code': 2049,
        'platform': 'iOS',
        'effected_regex_id': 0,
        'version': '1.33',
        'entity_id': '1970',
        'data': {
            'msg': _content,
            'link': _link
        },
        "scene": 1,
        'question': '',
        'sub_code': 5001,
        'seq': '18e93194-0738-11e8-9253-00163e0e09b9',
        'ssid': '0',
        'story_id': 18891,
        'intent_name': '',
        'template': '',
        'channel': 0,
        'effected_template_id': 0
    }


def get_media_data_by_media_id(_media_id: int) -> dict:
    """
    根据_media_id获取media_data
    :param _media_id: int
    :return: {
                "img": "", "media": "", "media_all": "", "media_title": ""
             }
    """

    sql = '''SELECT media_pic, media_oss_url, media_output_url, media_title
             FROM robot_media WHERE id = %d ''' % _media_id
    media_data = do_query_local_cache(
        db_name="db_robot",
        db_cfg="mysql.master",
        sql=sql, ex=60)

    media_dict = {}
    compress_value = "?x-oss-process=image/quality,q_30"
    if media_data:
        media_dict["img"] = media_data[0][0] or ""
        media_dict["compress_img"] = media_dict["img"] + compress_value
        media_dict["media"] = media_data[0][1] or ""
        try:
            media_dict["media_all"] = json.loads(media_data[0][2])
        except Exception as e:
            print("error message = ", str(e))
            media_dict["media_all"] = []
        media_dict["media_title"] = media_data[0][3] or ""
    return media_dict


def get_inner_content_by_media_id_and_type(
        _media_id: int, _media_type: int, _content: str = "",
        **kwargs) -> dict:
    """
    视频协议->2170, 音频->2180
    :param _media_id:
    :param _media_type: 2 -> 视频, 3 -> 音频, 5 -> 图文
    :param _content:
    :return:
    """
    inner_content_dict, data_dict, link_lst = {}, {}, []
    inner_content_dict["ssid"] = 0
    inner_content_dict["broadcast"] = 0
    inner_content_dict["sub_code"] = 0
    inner_content_dict["msg"] = ""
    inner_content_dict["seq"] = ""
    inner_content_dict["question"] = ""
    inner_content_dict["power"] = 4
    inner_content_dict["time"] = 1517474473
    inner_content_dict["scene"] = 1
    inner_content_dict["minute"] = "null"
    data_dict["home_name"] = ""
    data_dict["away_name"] = ""
    data_dict["home_team_id"] = 0
    data_dict["away_team_id"] = 0
    data_dict["season_id"] = 0
    data_dict["title"] = _content if _content else ""
    try:
        result_dict = get_media_data_by_media_id(_media_id)
    except Exception as e:
        print("Exception = {error_message}".format(error_message=str(e)))
        print("find no data!")
        result_dict = {}
    if _media_type == 2:
        inner_content_dict["code"] = 2170
        data_dict["count"] = 1
        data_dict["type"] = 1
        link_lst.append({"compress_img": result_dict.get("compress_img", ""),
                         "img": result_dict.get("img", "")})
        data_dict["media"] = result_dict.get("media", "")
        data_dict["media_all"] = result_dict.get("media_all")
        data_dict["media_title"] = result_dict.get("media_title", "")
        data_dict["link"] = link_lst
    elif _media_type == 3:
        inner_content_dict["code"] = 2180
        data_dict["media"] = result_dict.get("media", "")
        data_dict["media_title"] = result_dict.get("media_title", "")
    elif _media_type == 5:
        inner_content_dict["code"] = 2190
        data_dict["count"] = 1
        data_dict["type"] = 1
        link_lst.append({"compress_img": kwargs.get("_compress_img", ""),
                         "img": kwargs.get("_img", "")})
        data_dict["link"] = link_lst

    inner_content_dict["data"] = data_dict
    return inner_content_dict


def world_cup_get_team_info_by_name(_team_name: str) -> list:
    sql = "SELECT `team_id`, `cn_name` FROM `team` WHERE `cn_name` = \"%s\"" % _team_name

    return do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql, ex=36000)


def world_cup_query_season_name_by_season_id(_season_id: id) -> list:
    sql = "SELECT `cn_name` FROM `season` WHERE `season_id`=%d" % _season_id
    return do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql, ex=36000)


def world_cup_get_match_id_by_season_round_team(
        season_id: int, round_name: str, team_id: int) -> list:
    """根据世界杯赛季id+阶段名称+球队id查询比赛id列表"""
    match_id_lst = []
    if round_name:
        sql = '''select match_id from `match` where season_id = %d and 
        r_round_name = "%s" and (team_A_id = %d or 
        team_B_id = %d)''' % (season_id, round_name, team_id, team_id)
    else:
        sql = '''select match_id from `match` where season_id = %d and (team_A_id
                 = %d or team_B_id = %d)''' % (season_id, team_id, team_id)
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql, ex=3600)
    if results:
        for i in range(len(results)):
            match_id_lst.append(results[i][0])
    return match_id_lst


def world_cup_get_match(match_id: int):
    """
    通过match_id查询match记录
    :param match_id:
    :return:
    """
    sql = '''SELECT
      match_id      AS id,
      r_season_name AS season_name,
      r_round_name  AS round_name,
      team_A_id     AS home_id,
      team_B_id     AS away_id,
      team_A_name   AS home_name,
      team_B_name   AS away_name,
      fs_A          AS fs_home,
      fs_B          AS fs_away,
      ets_A         AS ets_home,
      ets_B         AS ets_away
    FROM
      `match`
    WHERE
      match_id={:d}'''.format(match_id)

    match_data = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)

    if match_data[0]['ets_home']:
        match_data[0]['home_score'] = match_data[0]['ets_home']
        match_data[0]['away_score'] = match_data[0]['ets_away']
    else:
        match_data[0]['home_score'] = match_data[0]['fs_home']
        match_data[0]['away_score'] = match_data[0]['fs_away']
    return match_data


def world_cup_get_match_list_by_two_team(team0_id: int, team1_id: int):
    """
    通过两个球队的team_id查询这两个球队历史上所有的比赛赛果
    :param team0_id:
    :param team1_id:
    :return:
    """
    sql = '''SELECT
      match_id      AS id,
      r_season_name AS season_name,
      r_round_name  AS round_name,
      team_A_id     AS home_id,
      team_B_id     AS away_id,
      team_A_name   AS home_name,
      team_B_name   AS away_name,
      fs_A          AS home_score,
      fs_B          AS away_score
    FROM
      `match`
    WHERE
      (team_A_id={0:d} AND team_B_id={1:d}) OR 
      (team_B_id={1:d} AND team_A_id={0:d})
    ORDER BY match_time DESC'''.format(team0_id, team1_id)

    match_data = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)
    return match_data


def world_cup_get_match_id_by_season_round(
        season_id: int, round_name: str) -> list:
    """根据世界杯赛季id+阶段名称查询比赛id列表"""
    match_id_lst = []
    if round_name:
        sql = '''select match_id from `match` where season_id = %d and
                 r_round_name = "%s" ''' % (season_id, round_name)
    else:
        sql = '''select match_id from `match` where season_id = %d''' % season_id
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=5)
    if results:
        for i in range(len(results)):
            match_id_lst.append(results[i][0])
    return match_id_lst


def world_cup_get_match_id_by_season(season_id: int) -> int:
    """根据世界杯赛季id查询该世界杯的决赛的matchid"""
    match_id = 0
    sql = '''select match_id from `match` where season_id = %d and 
             r_round_name = "决赛" ''' % season_id
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=5)
    if results:
        match_id = results[0][0]
    return match_id


def world_cup_get_last_match_id_by_team(team_id: int) -> int:
    """给出该球队最近的世界杯最后一场比赛的matchid"""
    match_id = 0
    sql = '''select match_id from `match` where team_A_id = %d or 
             team_B_id = %d order by match_time desc
             LIMIT 1  ''' % (team_id, team_id)
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=5)
    if results:
        match_id = results[0][0]
    return match_id


def world_cup_get_last_match_id_by_season_team(
        season_id: int, team_id: int) -> int:
    """某个球队和某届世界杯, 给出该届世界杯这个球队最后一场比赛的matchid"""
    match_id = 0
    sql = '''select match_id from `match` where season_id = %d and 
             (team_A_id = %d or team_B_id = %d) order by match_time desc
             LIMIT 1  ''' % (season_id, team_id, team_id)
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=5)
    if results:
        match_id = results[0][0]
    return match_id


def world_cup_get_match_lst_by_round(round_name: str) -> list:
    """只有某一阶段，则给最近的世界杯该阶段的matchid"""
    match_id_lst = []
    sql1 = '''select season_id from `match` where r_round_name = "%s"
              ORDER BY match_time desc limit 1''' % round_name
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql1,
        ex=5)
    if results:
        season_id = results[0][0]
        match_id_lst = world_cup_get_match_id_by_season_round(
            season_id, round_name
        )
    return match_id_lst


def world_cup_get_match_id_lst_by_round_team(
        round_name: str, team_id: int) -> list:
    """某一个阶段、哪支球队，则直接给予最近世界杯该球队这个阶段的赛果"""
    match_id_lst = []
    sql1 = '''select season_id from `match` where r_round_name = "%s" 
              and (team_A_id = %d or team_B_id = %d) ORDER BY match_time desc 
              limit 1''' % (round_name, team_id, team_id)
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql1,
        ex=5)
    if results:
        season_id = results[0][0]
        match_id_lst = world_cup_get_match_id_by_season_round_team(
            season_id, round_name, team_id
        )
    return match_id_lst


def world_cup_get_round_name_by_season_id(season_id: int) -> list:
    """通过 season_id 查询该世界杯所包含的所有的 round_name """
    round_name_lst = []
    sql = '''select distinct(r_round_name) from `match` where 
             season_id = %d''' % season_id
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600)
    if results:
        for i in range(len(results)):
            round_name_lst.append(results[i][0])
    return round_name_lst


def world_cup_get_team_roster_lst_by_season_team(
        season_id: int, team_id: int) -> list:
    """根据指定的赛季和球队id，查询球队大名单"""
    sql = '''SELECT table_a.cn_name AS nationality, table_a.person_id as id, 
             table_a.shirtnumber as number, squad.cn_name AS `name`, 
             squad.position as pos FROM (SELECT b.cn_name, 
             season_squad_stat.person_id, season_squad_stat.shirtnumber FROM 
             (SELECT team_id, cn_name FROM team WHERE team_id = %d) AS b 
             LEFT JOIN season_squad_stat ON b.team_id = season_squad_stat.team_id
             AND season_squad_stat.season_id = %d 
             ORDER BY season_squad_stat.shirtnumber) AS table_a INNER JOIN squad 
             ON table_a.person_id = squad.person_id ''' % (team_id, season_id)
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=5,
        use_dictcursor=True)
    return results


def world_cup_get_last_season_id_by_team(team_id: int) -> int:
    """给出该球队最近的世界杯的season_id"""
    season_id = 0
    sql = '''select season_id from `match` where team_A_id = %d or 
             team_B_id = %d order by match_time desc
             LIMIT 1  ''' % (team_id, team_id)
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=5)
    if results:
        season_id = results[0][0]
    return season_id


def world_cup_get_attend_team_lst_by_season_id(season_id: int) -> list:
    """通过指定赛季，查询参加世界杯球队列表"""
    sql = '''select a.team_id as team_id, team.cn_name as team_name, 
             a.result as rank from (select team_id, result from rel_season_team
             where season_id = %d) as a inner join team on 
             a.team_id = team.team_id ''' % season_id
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=5,
        use_dictcursor=True)
    return results


def world_cup_get_nation_name_by_person_id(person_id: int) -> str:
    """通过球员id查询该球员所属国家队名称"""
    nation_name = ''
    try:
        sql = '''select team.cn_name as cn_name from (select distinct(team_id) as 
                 team_id from rel_season_team_squad where person_id = %d) as a
                 left join team on a.team_id=team.team_id ''' % person_id
        results = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
        if results:
            nation_name = results[0][0]
    except Exception as e:
        print(str(e))
    return nation_name


def world_cup_get_player_red_yellow_card_rank(
        top: int = 5, _card: int = 1) -> list:
    """世界杯罚牌的球员top n"""
    player_ry_card_rank_lst = [['序号', '球员名', '罚牌次数', '所属国家']]
    if _card == 2:
        sql = '''select red_cards, a.person_id, b.cn_name 
                 from competition_squad_stat as a left join squad as b 
                 on a.person_id=b.person_id 
                 order by red_cards desc, appearances asc limit %d''' % top
    else:
        sql = '''select yellow_cards, a.person_id, b.cn_name 
                 from competition_squad_stat as a left join squad as b 
                 on a.person_id=b.person_id 
                 order by yellow_cards desc, appearances asc limit %d''' % top
    results = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    if results:
        for i in range(len(results)):
            player_ry_card_rank_lst.append([
                i + 1,
                results[i][2],
                results[i][0],
                world_cup_get_nation_name_by_person_id(results[i][1])
            ])
    return player_ry_card_rank_lst


def world_cup_get_player_appearance_rank(top: int = 5) -> list:
    """世界杯出场最多的球员top n"""
    player_appearance_rank_lst = [['序号', '球员名', '出场次数', '所属国家']]
    sql = '''select appearances, a.person_id, b.cn_name 
             from competition_squad_stat as a left join squad as b 
             on a.person_id=b.person_id 
             order by appearances desc, minutes_played desc 
             limit %d ''' % top
    results = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    if results:
        for i in range(len(results)):
            player_appearance_rank_lst.append([
                i + 1,
                results[i][2],
                results[i][0],
                world_cup_get_nation_name_by_person_id(results[i][1])
            ])
    return player_appearance_rank_lst


def world_cup_get_game_year_by_match_id(match_id: int) -> int:
    """通过球员id查询该球员所属国家队名称"""
    game_year = 0
    try:
        sql = '''SELECT r_season_name FROM `match` 
                 WHERE match_id = %d ''' % match_id
        results = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
        if results:
            game_year = int(results[0][0][:4])
    except Exception as e:
        print(str(e))
    return game_year


def world_cup_get_fast_goal_by_round(round_name: str = None) -> dict:
    """世界杯进球最快的进球"""
    result_dict = {}
    if round_name:
        sql = '''SELECT
                  event_code    AS code,
                  event_seconds AS r_event_seconds,
                  r_person_name AS player_name,
                  b.team_A_id   AS match_home_id,
                  b.team_B_id   AS match_away_id,
                  b.team_A_name AS match_home_name,
                  b.team_B_name AS match_away_name,
                  a.team_id     AS team_id,
                  IF( a.team_id = b.team_A_id, b.team_A_name, b.team_B_name 
                  )             AS team_name,
                  IF( a.team_id = b.team_A_id, b.team_B_name, b.team_A_name 
                  )             AS against_team_name,
                  a.match_id    AS match_id 
                 FROM
                   match_event a
                 LEFT JOIN `match` b ON a.match_id = b.match_id 
                 WHERE
                  event_code = 'G' AND r_round_name = "%s" 
                 ORDER BY
                  event_seconds 
                 LIMIT 1;''' % round_name
    else:
        sql = '''SELECT
                  event_seconds AS r_event_seconds,
                  r_person_name AS player_name,
                  b.team_A_id   AS match_home_id,
                  b.team_B_id   AS match_away_id,
                  b.team_A_name AS match_home_name,
                  b.team_B_name AS match_away_name,
                  a.team_id     AS team_id,
                  IF (a.team_id=b.team_A_id, b.team_A_name,b.team_B_name) 
                                AS team_name,
                  IF (a.team_id=b.team_A_id, b.team_B_name,b.team_A_name)
                                AS against_team_name,
                  a.match_id    AS match_id 
                  FROM match_event a 
                  LEFT JOIN `match` b ON a.match_id=b.match_id
                  WHERE event_code='G'
                  ORDER BY event_seconds
                  LIMIT 1;'''
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)
    if results:
        result_dict = results[0]
        result_dict['game_year'] = world_cup_get_game_year_by_match_id(
            results[0].get('match_id')
        )
    return result_dict


def world_cup_get_season_round_name_by_match_id(match_id: int) -> (str, str):
    """通过球员id查询该球员所属国家队名称"""
    season_name, round_name = '', ''
    try:
        sql = '''SELECT r_season_name, r_round_name FROM `match` 
                 WHERE match_id = %d ''' % match_id
        results = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
        if results:
            season_name, round_name = results[0][0], results[0][1]
    except Exception as e:
        print(str(e))
    return season_name, round_name


def world_cup_get_match_score_diff_rank_lst(top: int = 3) -> list:
    """世界杯比分悬殊最大的比赛，前3场"""
    match_score_diff_rank_lst = [['对阵球队', '比分', '年份', '阶段']]
    sql = '''select score_delta, b.match_id, b.team_A_name, b.team_B_name, 
             b.fs_A, b.fs_B, b.ets_A, b.ets_B from `match_score_stat` as a 
             left join `match` as b on a.match_id=b.match_id 
             order by score_delta desc, score_total desc 
             limit %d ''' % top
    results = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    if results:
        for i in range(len(results)):
            team_lst = [results[i][2], results[i][3]]
            season_round_name = world_cup_get_season_round_name_by_match_id(
                results[i][1]
            )
            if results[i][6]:
                score_list = [str(results[i][6]), str(results[i][7])]
            else:
                score_list = [str(results[i][4]), str(results[i][5])]
            match_score_diff_rank_lst.append([
                ' vs '.join(team_lst),
                ':'.join(score_list),
                season_round_name[0],
                season_round_name[1]
            ])
    return match_score_diff_rank_lst


def world_cup_get_match_by_goal_count_rank_lst(
        top: int = 3, round_name: str = None) -> list:
    """世界杯进球最多的比赛，前3场"""
    match_goal_count_rank_lst = [['对阵球队', '比分', '年份', '阶段']]
    if round_name:
        sql = '''select score_total, b.match_id, b.team_A_name, b.team_B_name, 
                 b.fs_A, b.fs_B, b.ets_A, b.ets_B from `match_score_stat` as `a` 
                 left join `match` as `b` on a.match_id=b.match_id 
                 where b.r_round_name="%s"
                 order by score_total desc, score_delta desc
                 limit %d ''' % (round_name, top)
    else:
        sql = '''select score_total, b.match_id, b.team_A_name, b.team_B_name, 
                 b.fs_A, b.fs_B, b.ets_A, b.ets_B from `match_score_stat` as `a` 
                 left join `match` as `b` on a.match_id=b.match_id 
                 order by score_total desc, score_delta desc
                 limit %d ''' % top
    results = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    if results:
        for i in range(len(results)):
            team_lst = [results[i][2], results[i][3]]
            season_round_name = world_cup_get_season_round_name_by_match_id(
                results[i][1]
            )
            if results[i][6]:
                score_list = [str(results[i][6]), str(results[i][7])]
            else:
                score_list = [str(results[i][4]), str(results[i][5])]
            match_goal_count_rank_lst.append([
                ' vs '.join(team_lst),
                ':'.join(score_list),
                season_round_name[0],
                season_round_name[1]
            ])
    return match_goal_count_rank_lst


def world_cup_get_session_id_by_year(year: int):
    sql = '''SELECT season_id
             FROM `match`
             WHERE r_season_name LIKE '{}%'
             LIMIT 1;'''.format(year)
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    return rslt


def world_cup_get_season_id_orderd_by_date():
    sql = '''SELECT @row:=@row+1 AS row, season_id
             FROM `season`, (SELECT CONVERT(@row:=0, UNSIGNED)) _
             ORDER BY start_date;'''
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    return rslt


def world_cup_get_goalscorers_list_by_season(season_id: int, top: int = 5):
    sql = '''SELECT
              @row:=@row+1 AS row,
              b.cn_name AS name,
              c.cn_name AS country,
              goals
             FROM
              (`season_squad_stat` AS a
               LEFT JOIN `squad` AS b ON a.person_id=b.person_id)
               LEFT JOIN `area` AS c ON b.nationality_id=c.area_id,
               (SELECT CONVERT(@row:=0, UNSIGNED)) _
             WHERE
              season_id={:d}
             ORDER BY
              goals DESC
             LIMIT {:d};'''.format(season_id, top)
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=5)
    return rslt


def world_cup_get_goalscorers_list_total(top: int = 5):
    sql = '''SELECT
              @row:=@row+1 AS row,
              b.cn_name    AS name,
              c.cn_name    AS country,
              goals
             FROM
              competition_squad_stat a
                LEFT JOIN squad b ON a.person_id = b.person_id
                LEFT JOIN area c ON b.nationality_id=c.area_id,
                (SELECT CONVERT(@row:=0, UNSIGNED)) _
             ORDER BY
              goals DESC,
              appearances ASC 
              LIMIT {:d};'''.format(top)
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    return rslt


def world_cup_get_fast_goal_rank(top: int = 5):
    sql = '''SELECT
              r_person_name,
              IF(a.team_id=b.team_A_id, b.team_A_name, b.team_B_name) AS country,
              event_seconds,
              IF(a.team_id=b.team_A_id, b.team_B_name, b.team_A_name) AS against
             FROM
              match_event AS a LEFT JOIN `match` AS b ON a.match_id = b.match_id
             WHERE
              event_code = 'G' 
             ORDER BY event_seconds 
             LIMIT {:d}'''.format(top)
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    return rslt


def world_cup_get_team_rank_by_goal(top: int = 10):
    sql = '''SELECT
              b.cn_name,
              IF(b.cn_name='德国', COUNT(DISTINCT (m.season_id))+10, 
               COUNT(DISTINCT (m.season_id))) AS worldcup_total,
              matches_total,
              goals_pro
             FROM
              competition_team_score_stat a
              LEFT JOIN team b ON a.team_id = b.team_id
              LEFT JOIN `match` m ON (
              b.team_id = m.team_B_id
              OR b.team_id = m.team_A_id
              )
             WHERE
              matches_total > 0
             GROUP BY
              b.cn_name
             ORDER BY
              goals_pro DESC,
              matches_total
             LIMIT {:d};'''.format(top)
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    return rslt


def world_cup_get_most_champion_team(top):
    sql = '''SELECT
              team_id,
              r_team_name AS team_name,
              trophy_num
             FROM
                competition_team_trophy_stat 
             WHERE
                trophy_type = 1 
             ORDER BY
                trophy_num DESC
             LIMIT {:d};'''.format(top)
    rslt = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)
    return rslt


def world_cup_get_most_second_palce_team(top):
    sql = '''SELECT
              team_id,
              r_team_name AS team_name,
              trophy_num
             FROM
              competition_team_trophy_stat 
             WHERE
              trophy_type = 2 
             ORDER BY
              trophy_num DESC
             LIMIT {:d};'''.format(top)
    rslt = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)
    return rslt


def world_cup_get_most_final_team(top):
    sql = '''SELECT
              team_id,
              r_team_name AS team_name,
              trophy_num
             FROM
              competition_team_trophy_stat 
             WHERE
              trophy_type = 3
             ORDER BY
              trophy_num DESC
             LIMIT {:d};'''.format(top)
    rslt = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=60,
        use_dictcursor=True)
    return rslt


def world_cup_get_season():
    sql = '''SELECT
              @row:=@row+1 AS number,
              LEFT(cn_name, 4) AS year,
              SUBSTRING(cn_name, 5) AS country,
              season_id
             FROM 
              season,
              (SELECT CONVERT(@row:=0, UNSIGNED)) _
             ORDER BY start_date;
              '''
    rslt = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)
    return rslt


def world_cup_get_season_id_by_host(host):
    sql = '''SELECT
              season_id
             FROM 
              season
             WHERE
              cn_name LIKE %{:s}
             ORDER BY start_date
             LIMIT 1;
             '''.format(host)
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    return rslt


def world_cup_get_season_id_by_host_and_year(host, year):
    sql = '''SELECT
              season_id
             FROM 
              season
             WHERE
              cn_name={:d}{:s}
          '''.format(year, host)
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    return rslt


def world_cup_get_rocord_event_goal_player_age(
        reverse_value: bool = False, round_name: str = None) -> dict:
    """查询世界杯进球球员年龄记录（进球年龄最大或最小进球球员）"""
    result_dict = {}
    if round_name:
        if reverse_value:
            sql = '''select  a.match_id as match_id, a.person_id as player_id, 
                     a.r_person_name as player_name, a.team_id as team_id, 
                     a.r_team_name as team_name, a.age_year as player_age_year,
                     a.age_day as player_age_day, b.team_A_id as match_home_id,
                     b.team_B_id as match_away_id, 
                     b.team_A_name as match_home_name, 
                     b.team_B_name as match_away_name 
                     from (select * from squad_score_age 
                     where r_round_name="%s" order by age_year, age_day 
                     limit 1) as a left join `match` as b 
                     on a.match_id = b.match_id ''' % round_name
        else:
            sql = '''select  a.match_id as match_id, a.person_id as player_id, 
                     a.r_person_name as player_name, a.team_id as team_id, 
                     a.r_team_name as team_name, a.age_year as player_age_year,
                     a.age_day as player_age_day, b.team_A_id as match_home_id,
                     b.team_B_id as match_away_id, 
                     b.team_A_name as match_home_name, 
                     b.team_B_name as match_away_name 
                     from (select * from squad_score_age 
                     where r_round_name="%s" 
                     order by age_year desc, age_day desc 
                     limit 1) as a left join `match` as b 
                     on a.match_id = b.match_id ''' % round_name
    else:
        if reverse_value:
            sql = '''SELECT  a.match_id AS match_id, a.person_id AS player_id, 
                     a.r_person_name AS player_name, a.team_id AS team_id, 
                     a.r_team_name AS team_name, a.age_year AS player_age_year,
                     a.age_day AS player_age_day, b.team_A_id AS match_home_id,
                     b.team_B_id AS match_away_id, 
                     b.team_A_name AS match_home_name, 
                     b.team_B_name AS match_away_name 
                     FROM (SELECT * FROM squad_score_age 
                     ORDER BY age_year, age_day 
                     LIMIT 1) AS a LEFT JOIN `match` AS b 
                     ON a.match_id = b.match_id '''
        else:
            sql = '''SELECT  a.match_id AS match_id, a.person_id AS player_id, 
                     a.r_person_name AS player_name, a.team_id AS team_id, 
                     a.r_team_name AS team_name, a.age_year AS player_age_year,
                     a.age_day AS player_age_day, b.team_A_id AS match_home_id,
                     b.team_B_id AS match_away_id, 
                     b.team_A_name AS match_home_name, 
                     b.team_B_name AS match_away_name 
                     FROM (SELECT * FROM squad_score_age 
                     ORDER BY age_year DESC, age_day DESC 
                     LIMIT 1) AS a LEFT JOIN `match` AS b 
                     ON a.match_id = b.match_id '''
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)
    if results:
        result_dict = results[0]
        result_dict['game_year'] = world_cup_get_game_year_by_match_id(
            results[0].get('match_id')
        )
    return result_dict


def world_cup_get_cn_position_from_mysql_table():
    """从mysql表中获取球员位置的翻译"""
    result_dict = {}
    sql = '''SELECT en_position, cn_position FROM position_table'''
    results = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)
    if results:
        for i in range(len(results)):
            result_dict[results[i]['en_position']] = results[i]['cn_position']
    return result_dict


def world_cup_get_all_year_season_name() -> dict:
    """从Mysql表中获取世界杯所有的举办时间和举办地"""
    result_dict = {}
    sql = '''SELECT cn_name FROM season'''
    results = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    for i in range(len(results)):
        result_dict[int(results[i][0][:4])] = results[i][0][4:]
    return result_dict


def world_cup_get_all_season() -> dict:
    """从Mysql表中获取世界杯所有的举办season"""
    result_dict = {}
    sql = '''SELECT cn_name, season_id FROM season'''
    results = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    for i in range(len(results)):
        result_dict[results[i][0]] = results[i][1]
    return result_dict


def world_cup_get_team_name_by_team_id(team_id: int) -> str:
    """根据team_id获取team_name"""
    team_name = ""
    sql = "SELECT cn_name FROM team WHERE team_id = %d" % team_id
    rslt = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)
    if rslt:
        team_name = rslt[0].get("cn_name")
    return team_name


def world_cup_get_season_name_by_season_id(season_id: int) -> str:
    """根据season_id获取season_name"""
    season_name = ""
    sql = "SELECT cn_name FROM team WHERE season_id = %d" % season_id
    rslt = do_query_local_cache(
        db_name="db_fifa_wordcup",
        db_cfg="mysql.world_cup",
        sql=sql,
        ex=3600,
        use_dictcursor=True)
    if rslt:
        season_name = rslt[0].get("cn_name")
    return season_name


@functools.lru_cache(512)
def world_cup_get_team_rank_total():
    rtn = {}
    sql = '''SELECT
              b.cn_name,
             IF(b.cn_name = '德国', COUNT(DISTINCT (m.season_id)) + 10,
                COUNT(DISTINCT (m.season_id)))               AS worldcup_total
             FROM
              team b
              LEFT JOIN `match` m ON (b.team_id = m.team_B_id OR b.team_id = 
                                      m.team_A_id)
             GROUP BY b.cn_name
             ORDER BY worldcup_total DESC;'''
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=3600)
    for _ in rslt:
        rtn[_[0]] = _[1]
    return rtn


def world_cup_get_team_group_rank_by_goal(top):
    sql = '''SELECT
              IF(r_team_name = '西德', '德国', r_team_name)  AS team_name,
              CONVERT(SUM(goals_pro), UNSIGNED)             AS total
             FROM
              team_table
             GROUP BY
              IF(r_team_name = '西德', '德国', r_team_name)
             ORDER BY
              total DESC
             LIMIT {:d};'''.format(top)
    rslt = do_query_local_cache(
            db_name="db_fifa_wordcup",
            db_cfg="mysql.world_cup",
            sql=sql,
            ex=60)
    world_cup_team_worldcup_total_dict = world_cup_get_team_rank_total()
    for _ in rslt:
        yield _[0], world_cup_team_worldcup_total_dict[_[0]], _[1]
