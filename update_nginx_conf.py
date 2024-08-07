'''
    Source create by Iwan Setiawan
    v1 : (2023 1th march)
        first release

        copy source code to : (create new folder)
        /etc/nginx/sites-available/auto-generate-nginx/
        
        result is auto generate to parent folder :
        /etc/nginx/sites-available/


'''

import sys
import os

def get_domain_list(file_list):
    f = open(file_list, "r")
    a = f.read()
    return a.split('\n')

def create_nginx_conf(file_list, nginx_conf):
    group_name = file_list.split('.')
    if len(group_name) >= 2:
        group_name = group_name[0]
        # print('group name no ext', group_name)

    group_name = group_name.split('-')
    if len(group_name) >= 3:
        group_name = group_name[len(group_name)-1]
    else:
        group_name = ''
        # print('group name', group_name)

    f = open(nginx_conf, "r")
    nginx_conf = f.read()
    # print('nginx-conf', nginx_conf)

    # get domain list
    mlist = get_domain_list(file_list) 

    for i in mlist:
        if i:
            if group_name:
                file_name = os.path.join('../', group_name + '-' + i.replace('.lombokbaratkab.go.id',''))
            else:
                file_name = os.path.join('../', i.replace('.lombokbaratkab.go.id',''))

            print('Proses', i, file_name)
                        
            f = open(file_name + '.conf', "w")

            tmp = nginx_conf.replace('[__server_name__]', i)            

            f.write(tmp)

            f.close()


def create_wsgi_daemon_conf():
    '''
        Create wsgi daemon and underconstruction page
    '''
    f = open('wsgi-daemon-conf.dat', "r")
    wsgi_conf = f.read()

    file_name = os.path.join('../', 'wsgi_daemon.conf')
    f = open(file_name, "w")    
    f.write(wsgi_conf)
    f.close()      
    
    # Default (underconstruction page)
    f = open('000-default-conf.dat', "r")
    wsgi_conf = f.read()

    file_name = os.path.join('../', '000-default.conf')
    f = open(file_name, "w")    
    f.write(wsgi_conf)
    f.close()      
                
def create_symlink(file_list):
    # get domain list
    mlist = get_domain_list(file_list) 

    # current_dir = os.getcwd()
    if not os.path.exists('../../sites-enabled'):
        os.mkdir('../../sites-enabled')

    for i in mlist:
        if i:   # not empty i
            file_name = i.replace('.lombokbaratkab.go.id','')
            print('Proses', file_name)
            tmp = os.path.join('../../sites-enabled',file_name)
            # print(tmp)
            # print(os.path.islink(tmp))
            if not os.path.islink(tmp):
                os.symlink(os.path.join('../', file_name), tmp)            

def create_symlink2_wsgi_daemon():
    file_name = 'wsgi_daemon.conf'
    if os.path.islink(file_name):
        os.remove(file_name)
        
    os.symlink(os.path.join('../sites-available',file_name), file_name)                            
    
    # underconstruction
    file_name = '000-default.conf'
    if os.path.islink(file_name):
        os.remove(file_name)
        
    os.symlink(os.path.join('../sites-available',file_name), file_name)                            
    
    
# jalankan di sites-enabled, copy dari source code
def create_symlink2(file_list_path):
    # get domain list
    mlist = get_domain_list(file_list_path) 

    # current_dir = os.getcwd()
    # if not os.path.exists('../../sites-enabled'):
    #     os.mkdir('../../sites-enabled')

    for i in mlist:
        if i:   # not empty i
            file_name = i.replace('.lombokbaratkab.go.id','')
            file_name = file_name + '.conf'
            print('Proses', file_name)
            # tmp = os.path.join(file_name)
            # print(tmp)
            # print(os.path.islink(tmp))
            
            # hapus target jika sudah ada link
            if os.path.islink(file_name):
                os.remove(file_name)
                
            # if not os.path.islink(file_name):
            os.symlink(os.path.join('../sites-available',file_name), file_name)                            

def help():
    print('')
    print('Help File :')
    print('-----------')
    print('Type:')
    print(' 1. > python update_nginx_conf.py domain-list nginx-conf')
    print('')
    print(' Where: ')
    print(' #. domain-list is get from site django project (if add new site, update this file too)')
    print(' #. nginx-conf is template for create nginx configuration, change this will update all other file generated by this command')
    print('')
    print(' 2. > python update_nginx_conf.py symlink domain-list')
    print('')
    print(' Where: ')
    print(' #. domain-list is file from django django site')
    print(' #. symlink is command to create symlink with relative path to current direktory')    
    print('')
    print(' Copy or create symlink update_nginx_conf.py from available to enable folder an run :')
    print(' 3. > python update_nginx_conf.py domain-list')
    print('')
    print(' Where: ')
    print(' #. domain-list is file from django django site')
    print(' #. This command should work, not like command 2')    
    print('')
    print('-----------')
    print('')

if __name__=='__main__':
    m_len = len(sys.argv)
    # print(m_len)
    # print(sys.argv[0])

    if m_len>=3:        
        if sys.argv[1]=='symlink':
            create_symlink(sys.argv[2])         # deprecated
            print('Done...')
        else:
            print(sys.argv[1], sys.argv[2])        
            create_nginx_conf(sys.argv[1], sys.argv[2])
            create_wsgi_daemon_conf()
            print('Done...')
    elif m_len>=2:        
        create_symlink2(sys.argv[1])        
        create_symlink2_wsgi_daemon()
        print('Done...')
    else:
        help()
