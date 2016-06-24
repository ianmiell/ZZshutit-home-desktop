"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule
import random
import string

class shutit_home_setup(ShutItModule):

	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches)
		#                                    - Returns True if any lines in output match any of
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		#
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#                                    - Delete text from file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#                                    - Replace text from file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		#
		# USER INTERACTION
		# shutit.get_input(msg,default,valid[],boolean?,ispass?)
		#                                    - Get input from user and return output
		# shutit.fail(msg)                   - Fail the program and exit with status 1
		#
		vagrant_image = shutit.cfg[self.module_id]['vagrant_image']
		vagrant_provider = shutit.cfg[self.module_id]['vagrant_provider']
		gui = shutit.cfg[self.module_id]['gui']
		memory = shutit.cfg[self.module_id]['memory']
		module_name = 'shutit_home_setup_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
		shutit.send('rm -rf /tmp/' + module_name + ' && mkdir -p /tmp/' + module_name + ' && cd /tmp/' + module_name)
		shutit.send('vagrant init ' + vagrant_image)
		print memory
		shutit.send_file('/tmp/' + module_name + '/Vagrantfile','''
Vagrant.configure(2) do |config|
  config.vm.box = "''' + vagrant_image + '''"
  # config.vm.box_check_update = false
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  # config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.network "public_network"
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = ''' + gui + '''
    vb.memory = "''' + memory + '''"
    vb.name = "shutit_home_setup"
  end
end''')
		shutit.send('vagrant up --provider virtualbox',timeout=99999)
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant')

		# TODO
		#git repos
		#flash player?
		#google chrome?
		shutit.send('apt-get upgrade -y')
		shutit.install('git')
		shutit.install('docker.io')
		shutit.install('python-pip')
		shutit.install('vim')
		shutit.install('meld')
		shutit.install('run-one')
		shutit.install('libreoffice')
		shutit.install('lubuntu-desktop')
		shutit.install('gnome-terminal')
		shutit.install('virtualbox-guest-dkms')
		shutit.install('virtualbox-guest-additions-iso')
		shutit.install('virtualbox-guest-utils')
		shutit.install('virtualbox-guest-x11')
		#shutit.install('ubuntu-restricted-extras')
		#shutit.install('libavcodec-extra')
		#shutit.install('libdvd-pkg')
		shutit.install('pychecker')
		shutit.install('apt-file')
		shutit.install('html2text')
		shutit.send('pip install shutit')
		shutit.send('apt-file update')

		shutit.send('useradd -m -s /bin/bash imiell')
		shutit.send('usermod -G sudo -a imiell')
		shutit.send('usermod -G docker -a imiell')
		shutit.send('mkdir -p /space/git')
		shutit.send('chown -R imiell: /space')
		shutit.set_password(shutit.cfg[self.module_id]['imiellpass'], user='imiell')
		
		shutit.login(command='su - imiell')
		
		shutit.send('cd /space/git')
		shutit.send('git clone --depth=1 https://github.com/ianmiell/shutit')
		shutit.send('git clone --depth=1 https://github.com/ianmiell/shutit-templates')
		shutit.multisend('git clone --depth=1 ssh://imiell@shutit.tk:/var/cache/git/work.git',{'assword':shutit.cfg[self.module_id]['shutittkpass'],'continue connecting':'yes'})

		shutit.send('git clone --depth=1 https://github.com/ianmiell/dotfiles ~imiell/.dotfiles')
		shutit.send('cd ~/.dotfiles')
		shutit.multisend('./script/bootstrap',{'author name':'Ian Miell','author email':'ian.miell@gmail.com','want to do':'o'})
		shutit.send('local-gen')
		shutit.send('localectl set-locale LANG="en_GB.UTF-8"')
		#shutit.multisend('ssh-keygen -f ~/.ssh/id_dsa',{'empty for no':''})
		#shutit.send('docker pull imiell/docker-dev-tools-image')

		shutit.logout()
		shutit.logout()
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		shutit.get_config(self.module_id,'vagrant_image',default='ubuntu/xenial64')
		shutit.get_config(self.module_id,'vagrant_provider',default='virtualbox')
		shutit.get_config(self.module_id,'shutittkpass')
		shutit.get_config(self.module_id,'imiellpass')
		shutit.get_config(self.module_id,'gui')
		shutit.get_config(self.module_id,'memory',default='3072')
		return True




def module():
	return shutit_home_setup(
		'imiell.shutit_home_setup.shutit_home_setup', 1231871956.0001,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup','shutit-library.virtualbox.virtualbox.virtualbox','tk.shutit.vagrant.vagrant.vagrant']
	)
