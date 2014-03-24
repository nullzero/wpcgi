class NotApprovedError(Exception):
    flash_msg = 'core-user-not-approved'
    flash_level = 'danger'

class IDNotFoundError(Exception):
    flash_msg = 'categorymover-id-not-found'
    flash_level = 'danger'
