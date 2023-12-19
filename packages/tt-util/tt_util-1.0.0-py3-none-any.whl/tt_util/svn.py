import logging
import subprocess


class SVNClient:
    """
    :param repo_url:     string      svn地址
    :param working_copy_path: string     检出地址
    :param username: string     用户名
    :param password: string     密码
    :return output: string      日志
    :return error: string      错误
    :return returncode: string      返回码
    """
    def __init__(self, repo_url: str, working_copy_path: str, username: str, password: str):
        self.repo_url = repo_url
        self.working_copy_path = working_copy_path
        self.username = username
        self.password = password

    def execute_svn_command(self, command):
        full_command = f'svn {command}'
        process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return output.decode('utf-8'), error.decode('utf-8'), process.returncode

    def checkout(self):
        return self.execute_svn_command(
            f'checkout {self.repo_url} {self.working_copy_path} --username={self.username} --password={self.password}')

    def update(self):
        return self.execute_svn_command(
            f'update {self.working_copy_path} --username={self.username} --password={self.password}')

    def add(self, route: str):
        return self.execute_svn_command(
            f'add {route}')

    def commit(self, message: str):
        return self.execute_svn_command(
            f'commit -m "{message}" {self.working_copy_path} --username={self.username} --password={self.password}')


if __name__ == '__main__':
    # 使用示例
    svn_client = SVNClient(repo_url='svn://', working_copy_path='', username='',
                           password='')
    checkout_output, checkout_error, checkout_code = svn_client.checkout()
    logging.info(f'检出日志: {checkout_output}')
    logging.error(f'检出错误: {checkout_error}')
    logging.info(f'检出返回码: {checkout_code}')

    update_output, update_error, update_code = svn_client.update()
    logging.info(f'更新日志: {update_output}')
    logging.error(f'更新错误: {update_error}')
    logging.info(f'更新返回码: {update_code}')

    add_output, add_error, add_code = svn_client.add("/app/temp/svn/nginx/2")
    logging.info(f'增加日志: {add_output}')
    logging.error(f'增加错误: {add_error}')
    logging.info(f'增加返回码: {add_code}')

    commit_output, commit_error, commit_code = svn_client.commit('Committing changes')
    logging.info(f'提交日志: {commit_output}')
    logging.error(f'提交错误: {commit_error}')
    logging.info(f'提交返回码: {commit_code}')
