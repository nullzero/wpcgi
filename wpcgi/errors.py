class NotApprovedError(Exception):
    flash_msg = 'error-user-not-approved'
    flash_level = 'danger'

class IDNotFoundError(Exception):
    flash_msg = 'error-id-not-found'
    flash_level = 'danger'
