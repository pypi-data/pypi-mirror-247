import subprocess as sp
from clera import *

def deploy():
    try:
        window = Window(fixed_size=(200, 129), frame=False)
        Titlebar('Deploy')
        def select_file():
            filter  = '(Python: *.py)'
            path, extention = File().open(filter=filter)
            
            GET('PATH').value(path)

        def deploy_project():
            name = GET('NAME')
            path = GET('PATH')

            if len(str(path)) != 0:
                print('[DEPLOY] Deploying application')
                with open('std.txt', 'w') as file:
                    window.quit()
                    sp.run("echo y |" + f' pyside6-deploy --name "{name}" {path}', shell=True, stdout=file)
                
                print('[DEPLOY] Executed file created ')
                sp.getoutput('python deploy.py')
            else:
                ...
        layout = [
            [Input('Application Name', 'NAME')],
            [Input('Path', 'PATH', readonly=True), Button('Browse', select_file)],
            [Button('DEPLOY', deploy_project)]
        ]

        Box(layout)
        window.run()
    except:
        print('[DEPLOY]: An Error Occured')
        