from enum import Enum

class SumRedEnum(str, Enum):
    SUM = "SUM"
    RED = "RED"

class ColumnUserMetricEnum(str, Enum):
    post_count = "post_count"
    favorite_post_count = "favorite_post_count"
    comment_count = "comment_count"
    favorite_comment_count = "favorite_comment_count"
    follower_count = "follower_count"
    followed_count = "followed_count"
    share_count = "share_count"
    connection_count = "connection_count"
    blocked_count = "blocked_count"
    reaction_comment_given_count = "reaction_comment_given_count"
    reaction_comment_received_count = "reaction_comment_received_count"
    enterprise_follow_count = "enterprise_follow_count"
    enterprise_follower_count = "enterprise_follower_count"
    profile_view_count = "profile_view_count"
    vacancy_application_count = "vacancy_application_count"