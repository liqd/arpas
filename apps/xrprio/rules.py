import rules

from adhocracy4.modules import predicates as module_predicates

rules.add_perm(
    "a4_candy_xrprio.add_topic", module_predicates.is_allowed_moderate_project
)

rules.add_perm(
    "a4_candy_xrprio.change_topic", module_predicates.is_allowed_moderate_project
)

rules.add_perm(
    "a4_candy_xrprio.view_topic",
    (
        module_predicates.is_allowed_moderate_project
        | module_predicates.is_allowed_view_item
    ),
)

rules.add_perm("a4_candy_xrprio.rate_topic", module_predicates.is_allowed_rate_item)

rules.add_perm(
    "a4_candy_xrprio.comment_topic", module_predicates.is_allowed_comment_item
)
