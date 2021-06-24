from pathlib import Path

def pathCache():
    '''
    Create pathCache directory
    '''
    path= Path('src/cache')
    if not path.exists():
        path.mkdir()

    return path

