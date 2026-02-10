import os
from typing import Optional


def create_dir(path: Optional[str]=None, chmod_mode: Optional[int]=None,gid: Optional[int]=None, uid: Optional[int]=None) -> None:
    import pwd, grp
    if chmod_mode is None:
        chmod_mode = 0o775
    if gid is None:
        gid = grp.getgrnam(os.getlogin()).gr_gid
    if uid is None:
        uid = pwd.getpwnam(os.getlogin()).pw_uid
    if not os.path.exists(path):
        os.makedirs(path)
        os.chmod(path, chmod_mode)
        os.chown(path, gid, uid)

def create_file(path: Optional[str]=None, chmod_mode: Optional[int]=None,gid: Optional[int]=None, uid: Optional[int]=None) -> None:
    import pwd, grp
    if chmod_mode is None:
        chmod_mode = 0o775
    if gid is None:
        gid = grp.getgrnam(os.getlogin()).gr_gid
    if uid is None:
        uid = pwd.getpwnam(os.getlogin()).pw_uid
    if not os.path.exists(path):
        open(path, 'a').close()
        os.chmod(path, chmod_mode)
        os.chown(path, gid, uid)