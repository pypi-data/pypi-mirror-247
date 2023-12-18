import click

from asmrmanager.cli.core import rj_argument
from asmrmanager.common.rj_parse import RJID
from asmrmanager.logger import logger


@click.command()
@rj_argument
@click.option("-s", "--star", type=int, help="must be integer in [1, 5]")
@click.option("-c", "--comment", type=str)
def review(rj_id: RJID, star: int, comment: str):
    """review an ASMR with star(1-5) and comment and add it to storage path"""
    logger.info(
        f"run command review with rj_id={rj_id}, star={star} comment={comment}"
    )

    from asmrmanager.cli.core import create_database, fm

    db = create_database()

    update_stored = False
    if not fm.could_store():
        logger.warning(
            "storage/download path not found skip storing operation"
        )
    else:
        fm.store(rj_id)
        update_stored = True
    db.update_review(rj_id, star, comment, update_stored=update_stored)
    db.commit()
