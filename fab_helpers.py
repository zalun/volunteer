from fabric.api import env, local, run


def ve_prepare_cmd(cmd):
    """Switch to virtual environment and before command
    """
    return """
           export WORKON_HOME=%s &&
           source %s &&
           workon %s &&
           %s
           """ % (env.workondir, env.ve_wrapper, env.virtualenv, cmd)


def ve_local(cmd, *args, **kwargs):
    return local(ve_prepare_cmd(cmd), *args, **kwargs)


def ve_run(cmd, *args, **kwargs):
    return run(ve_prepare_cmd(cmd), *args, **kwargs)
