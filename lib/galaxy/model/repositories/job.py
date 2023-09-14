from sqlalchemy.sql.expression import (
    null,
    or_,
    select,
    true,
)

from galaxy.model import (
    Job,
    User,
    YIELD_PER_ROWS,
)
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class JobRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, Job)

    def get_jobs_to_check_at_startup(self, track_jobs_in_database: bool, config):
        if track_jobs_in_database:
            in_list = (Job.states.QUEUED, Job.states.RUNNING, Job.states.STOPPED)
        else:
            in_list = (Job.states.NEW, Job.states.QUEUED, Job.states.RUNNING)

        stmt = (
            select(Job)
            .execution_options(yield_per=YIELD_PER_ROWS)
            .filter(Job.state.in_(in_list) & (Job.handler == config.server_name))
        )
        if config.user_activation_on:
            # Filter out the jobs of inactive users.
            stmt = stmt.outerjoin(User).filter(or_((Job.user_id == null()), (User.active == true())))

        return self.session.scalars(stmt)
