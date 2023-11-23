import os
def linux_account_check(user_name,user_pwd):
    if user_name != "root":
        check=os.system(f"echo '{user_pwd}' |su  checkpass -c 'su -c echo {user_name}'")
        if check == 0 :
            l_success_msg = 'Success'
        else:
            l_success_msg = 'Failed'
        return l_success_msg
        print(check)
    else:
        return 'Failed'

def linux_admin(user_name,user_pwd):
    if user_name != "root" and user_name == "admin":
        check=os.system(f"echo '{user_pwd}' |su  checkpass -c 'su -c echo {user_name}'")
        if check == 0 :
            l_success_msg = 'Success'
        else:
            l_success_msg = 'Failed'
        return l_success_msg
        print(check)
    else:
        return 'Failed'